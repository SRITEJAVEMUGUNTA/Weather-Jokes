'''
Sriteja Vemugunta
Setup: After replacing the api_key and the password, one can access the program.
The program itself takes in user input of a location and returns the weather of the location with a funny script
 of length 150-300 words.

Hardest part: The hardest part of the program was being able to make succesive calls to both APIs, the
weather stack API and OpenAI API. However, by mapping out the process logically I was able to fix my problem.
'''


import requests
import openai
from datetime import datetime


# Set your WeatherStack API key here
weather_api_key = "WEATHER_STACK_API_KEY"

def getWeather(location):
    base_url = "http://api.weatherstack.com/current"
    params = {
        "access_key": weather_api_key,
        "query": location
    }
    response = requests.get(base_url, params=params).json()
    
    data = response

    # Get important data
    location = data.get('location', {}).get('name', 'Unknown Location')
    temperature = data.get('current', {}).get('temperature', 'N/A')
    description = data.get('current', {}).get('weather_descriptions', ['N/A'])[0]
    humidity = data.get('current', {}).get('humidity', 'N/A')
    precipitation = data.get('current', {}).get('precip', 'N/A')
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"Current Date/Time: {current_date}\n"  # Include the current date
    report += f"Weather in {location}:\n"
    report += f"Temperature: {temperature}°C\n"
    report += f"Description: {description}\n"
    report += f"Humidity: {humidity}%\n"
    report += f"Precipitation: {precipitation} mm\n"
        
    return(report)


# Filler for your own OpenAI API key
api_key = "OPENAI_API_KEY"
openai.api_key = api_key

# Initialize and define the array for reinforcement learning
conversation_history = []

# Function to generate a funny script based on a weather report
def generate_funny_script(weather_report):
    conversation_history.clear()

    # Function to get OpenAI's response
    def get_openai_response(prompt, conversation_history):
        conversation_history.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )

        return response.choices[0].message["content"]

    # Generate a funny script based on the weather report
    prompt = f"Write me a funny script based on the weather report. But only include the script and not a description of the set. Do not make a name for the reporter. {weather_report}"
    ai_response = get_openai_response(prompt, conversation_history)

    if ai_response is not None:
        # Limit the response to 150-300 words
        script_words = ai_response.split()
        if len(script_words) < 150:
            return "The response is too short to be funny. Please try again with a different weather report."
        else:
            return " ".join(script_words[:300])  # Limit the response to 300 words
    else:
        return "Unable to generate a funny script at the moment."

# Example usage of the function
location = input("Enter a location to get a funny weather report(City, Country/State): ")
print('\n')
weather_report = getWeather(location)
funny_script = generate_funny_script(weather_report)
print("Funny Script:")
print('\n')
print(funny_script)

    