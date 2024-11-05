# Mental Health Resource Finder

This project is a Python-based application designed to recommend mental health resources based on user-provided location, specialty, and risk level. It leverages OpenAI's `gpt-4o-mini` model to generate compassionate, location-based recommendations.

## Features

- **Custom Resource Loading**: Loads resources from a CSV file (`merged_data_with_resources.csv`) containing data on mental health resources.
- **Risk Assessment**: Calculates risk levels based on data and categorizes resources as Low, Normal, or High Risk.
- **Personalized AI-Powered Suggestions**: Uses OpenAI's `gpt-4o-mini` model to provide suggestions with an empathetic, supportive response tailored to the user's location and mental health needs.
- **Retry Mechanism**: Handles API rate limits and retries requests when needed.

## Getting Started

### Prerequisites

1. **Python 3.8 or higher**: [Download Python](https://www.python.org/downloads/)
2. **OpenAI API Key**: Get an API key from [OpenAI](https://platform.openai.com/account/api-keys)
3. **Libraries**: Install required libraries
   ```bash
   pip install openai pandas python-dotenv
   ```

### Environment Variables

Create a `.env` file in the project root to store your OpenAI API key securely:

```plaintext
OPENAI_API_KEY=your_openai_api_key_here
```

### CSV File Format

The application expects a CSV file named `merged_data_with_resources.csv` with the following columns:

- `Name`: Name of the resource
- `Type`: Type of service provided
- `Location`: City or state location
- `Specialty`: Type of mental health support offered (e.g., Anxiety, Depression)
- `Contact`: Contact information
- `Data_Value`: Numeric value used to assess risk level

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/jonahrahn/LLM-for-Mental-Health-resource-.git
   cd mental-health-resource-finder
   ```

2. **Install Dependencies**
   ```bash
   pip install dependencies
   ```

3. **Set Up Environment Variables**  
   Create a `.env` file and add your OpenAI API key as shown above.

### Running the Application

To start the application, run:

```bash
python main.py
```

The application will prompt you to enter a location and a type of support (e.g., Anxiety, Depression). If no resources are found locally, the AI will generate a recommendation.

## Code Overview

- **load_resources**: Loads data from a CSV file and calculates risk levels.
- **generate_openai_response**: Generates suggestions for resources using OpenAI’s `gpt-4o-mini` model.
- **display_resources**: Filters resources based on location and specialty and displays recommendations.
- **main**: Entry point of the program, which takes user input and calls the relevant functions.

## Example Output

```
Enter your location (e.g., city or state): New York
Enter the type of support you need (e.g., Anxiety, Depression): Anxiety

Name: New York Counseling Center
Type: In-person Counseling
Location: New York, NY
Specialty: Anxiety
Contact: (123) 456-7890
Risk Level: Low Risk
...
```

If no resources are found in the specified location, a response like this is generated:

```
No resources found for the specified criteria in your area.
AI Recommendation:
There are online counseling services available that can provide support for anxiety in your area. You may also consider national helplines or virtual therapy options to get the help you need.
```

## Error Handling

The application includes error handling for:
- **FileNotFoundError**: If the CSV file is missing, the application will prompt the user to ensure the file is available.
- **Rate Limit Exceeded**: If the OpenAI API rate limit is exceeded, the application will wait and retry.
- **OpenAI API Errors**: Logs any errors encountered during OpenAI API requests.

## Conclusion

The Mental Health Resource Finder provides an essential service by helping users find relevant mental health resources based on their location, specialty, and assessed risk level. By leveraging OpenAI’s gpt-4o-mini model, the tool offers empathetic and tailored recommendations, filling an important gap in accessible mental health support. This project aims to improve accessibility to mental health resources, especially in underserved areas, by making it easy to find relevant services based on user needs.

## Opportunities for Future Development

The following areas present opportunities to expand and enhance the functionality of this project:

	1.	Expanded Data Sources: Integrating additional data sources, such as regional or global mental health databases, can provide a more comprehensive list of resources and cover a broader range of services.
	2.	Automated Data Updates: Implementing a system to periodically update resource data could ensure that information remains current, improving the reliability of recommendations.
	3.	Enhanced Filtering Options: Allowing users to filter resources based on criteria such as insurance compatibility, cost, language preferences, and telehealth options could increase the relevance of recommendations.
	4.	User Feedback and Rating System: Adding a feedback mechanism for users to rate and review resources could improve recommendation accuracy over time and provide valuable insights for other users.
	5.	Multilingual Support: Expanding language support could make the tool accessible to a wider audience, offering recommendations in the user’s preferred language.
	6.	Mobile Application Development: Creating a mobile app version would make the tool more accessible for users on the go, especially beneficial for those in remote areas with limited access to mental health services.
	7.	Risk Analysis Customization: Adding user inputs for self-assessed mental health needs or linking to wearable data for a more personalized risk analysis could offer tailored recommendations that better align with each user’s mental health status.
	8.	Advanced AI Integration: Integrating advanced AI models, such as sentiment analysis on user inputs, could refine the recommendation approach by assessing urgency or tone to better support those in crisis.
