import os
import openai
import pandas as pd
import logging
import json
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up logging for debugging
logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s")

# Validate API Key
if not OPENAI_API_KEY:
    logging.error("Error: OPENAI_API_KEY is not set. Please add it to your environment variables.")
    exit(1)

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Load resources from CSV
def load_resources(file_path="merged_data_with_resources.csv"):
    try:
        resources = pd.read_csv(file_path)
        min_value = resources['Data_Value'].min()
        max_value = resources['Data_Value'].max()
        range_per_group = (max_value - min_value) / 3
        low_risk_threshold = min_value + range_per_group
        normal_risk_threshold = min_value + 2 * range_per_group

        resources['Risk Level'] = resources['Data_Value'].apply(
            lambda x: "Low Risk" if x < low_risk_threshold else "Normal Risk" if x < normal_risk_threshold else "High Risk"
        )
        return resources
    except FileNotFoundError:
        logging.error("Resource file not found. Please ensure 'Resources.csv' is available.")
        return None


def parse_json_response(response_text, location, specialty, risk_level):
    """
    Parses JSON response from OpenAI and returns it as a list of dictionaries.
    Adds the 'Location', 'Specialty', and 'Risk Level' fields to each item.
    """
    try:
        # Load JSON response
        resources = json.loads(response_text)
        
        # Add additional fields to each resource
        for resource in resources:
            resource['Location'] = location
            resource['Specialty'] = specialty
            resource['Risk Level'] = risk_level
        
        # Print parsed resources for debugging
        print(f"Parsed resources: {resources}")
        return resources
    except json.JSONDecodeError:
        logging.error("Failed to parse JSON response. The response may not be formatted correctly.")
        return []

# Generate a structured JSON response using OpenAI API
def generate_openai_response(location, specialty, risk_level):
    prompt = (
        f"A user is searching for mental health resources in {location}, "
        f"which has been identified as a '{risk_level}' area for mental health needs. "
        f"They are looking for support specializing in {specialty}. "
        "Please suggest options, prioritizing local resources first. If no local services are available, "
        "include national or online resources. Respond with empathy and support, reassuring the user "
        "that help is available, especially given the mental health needs in their area."
    )
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant providing mental health resource suggestions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        response_text = response.choices[0].message.content.strip()
        
        # Print response_text for debugging
        print("Raw response text:", response_text)

        # Try parsing as JSON if it's expected as JSON
        try:
            parsed_response = json.loads(response_text)
            print("Parsed JSON response:", parsed_response)
            return parsed_response
        except json.JSONDecodeError:
            logging.error("Failed to parse JSON response. The response may not be formatted correctly.")
            return response_text  # Return the raw text if JSON parsing fails

    except openai.OpenAIError as e:
        logging.error(f"Error generating OpenAI response: {e}")
        return "Unable to provide a tailored suggestion at the moment. Please refer to national helplines or online resources."

# Function to append new data to the CSV file in the required structure
def append_to_csv(file_path, new_data):
    """
    Appends new data to the specified CSV file, filling only the resource-related columns
    and maintaining the other columns as empty or with default values.
    """
    try:
        # Load the existing data
        existing_data = pd.read_csv(file_path)

        # Convert the new data to a DataFrame and add missing columns to match the existing file structure
        new_data_df = pd.DataFrame(new_data)
        required_columns = existing_data.columns
        for col in required_columns:
            if col not in new_data_df.columns:
                new_data_df[col] = None  # Fill missing columns with None

        # Reorder columns to match the existing file structure
        new_data_df = new_data_df[required_columns]

        # Check for duplicates based on 'Name' and 'Contact'
        combined_data = pd.concat([existing_data, new_data_df]).drop_duplicates(subset=["Name", "Contact"], keep="first")

        # Save the updated data back to the CSV
        combined_data.to_csv(file_path, index=False)
        logging.info(f"New resources appended to {file_path} successfully.")
        print(f"Appended new resources to {file_path}.")  # Confirmation print
    except FileNotFoundError:
        # If the CSV doesn't exist, create it with the new data
        new_data_df.to_csv(file_path, index=False)
        logging.info(f"{file_path} created with new resources.")
        print(f"Created new file {file_path} with resources.")  # Confirmation print    try:
        # Display the new data for verification
        new_data_df = pd.DataFrame(new_data)
        print("New data to append:\n", new_data_df)  # Debugging step

        # Load the existing CSV if it exists
        if os.path.exists(file_path):
            existing_data = pd.read_csv(file_path)
            print("Existing data in file before appending:\n", existing_data.head())  # Debugging step

            # Concatenate and remove duplicates based on 'Name' and 'Contact'
            combined_data = pd.concat([existing_data, new_data_df]).drop_duplicates(subset=["Name", "Contact"], keep="first")
        else:
            # If the file does not exist, simply use new_data_df
            combined_data = new_data_df

        # Save the combined data back to the CSV
        combined_data.to_csv(file_path, index=False)
        logging.info(f"New resources appended to {file_path} successfully.")
        print(f"Appended new resources to {file_path}.")  # Confirmation print
    except Exception as e:
        logging.error(f"Failed to append data to {file_path}: {e}")
        print(f"Error: Could not append data to {file_path}. Check log for details.")


# Display resources or call OpenAI API for suggestions
def display_resources(resources, location, specialty):
    filtered_resources = resources[
        resources['Location'].str.contains(location, case=False, na=False) & 
        resources['Specialty'].str.contains(specialty, case=False, na=False)
    ]
    
    if filtered_resources.empty:
        risk_level = "Normal Risk"  # Default if no specific data
        print("No resources found for the specified criteria in your area.")
        print(generate_openai_response(location, specialty, risk_level))
    else:
        for _, row in filtered_resources.iterrows():
            print(f"Name: {row['Name']}")
            print(f"Type: {row['Type']}")
            print(f"Location: {row['Location']}")
            print(f"Specialty: {row['Specialty']}")
            print(f"Contact: {row['Contact']}")
            print(f"Risk Level: {row['Risk Level']}\n")

# Main function
def main():
    resources = load_resources()
    if resources is None:
        return

    location = input("Enter your location (e.g., city or state): ")
    specialty = input("Enter the type of support you need (e.g., Anxiety, Depression, Crisis Intervention): ")

    display_resources(resources, location, specialty)

if __name__ == "__main__":
    main()