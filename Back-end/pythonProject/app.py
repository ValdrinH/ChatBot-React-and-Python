from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import requests
from fuzzywuzzy import fuzz
from sympy import sympify
import math

app = Flask(__name__)
CORS(app)
# Define intents and responses
intents = {
    'greeting': {
        'examples': ['hello', 'hi', 'hey'],
        'responses': [
            'Hello there! Welcome to our service. How can I assist you today?',
            'Hi there! Thanks for reaching out. How can I help you?',
            'Hey! It’s great to see you. How can I assist you today?'
        ]
    },
    'goodbye': {
        'examples': ['bye', 'goodbye', 'see you later'],
        'responses': [
            'Goodbye! Have a wonderful day!',
            'Take care! See you soon.',
            'See you later! Remember, we’re here whenever you need assistance.'
        ]
    },
    'weather': {
        'examples': ['weather', 'forecast', 'how is the weather today'],
        'responses': [
            'The weather forecast is available on our website. Feel free to check it out anytime!',
            'You can check the weather forecast online. Our website provides detailed updates.',
            'Our website offers comprehensive weather forecasts. Visit us to stay informed!'
        ]
    },
    'thanks': {
        'examples': ['thank you', 'thanks', 'thanks a lot'],
        'responses': [
            'You\'re welcome! It was my pleasure to assist you.',
            'No problem at all! Happy to help.',
            'Thank you for reaching out. If you need anything else, don\'t hesitate to ask!'
        ]
    },
    'location': {
        'examples': ['location','where are you?', 'what is your location?', 'from where are you?'],
        'responses': [
            'I am a virtual assistant and do not have a physical location.',
            'I exist in the digital realm.',
            'My location is wherever you need me to be.'
        ]
    },
    'help': {
        'examples': ['help', 'can you help me?', 'need assistance'],
        'responses': [
            'Of course! What do you need help with?',
            'I am here to assist you. Please let me know what you need.',
            'How can I assist you today?'
        ]
    },
    'news': {
        'examples': ['news', 'latest news', 'news update'],
        'responses': [
            'You can find the latest news on our website.',
            'Our website provides the latest news updates.',
            'Stay tuned for the latest news on our website.'
        ]
    },
    'faq': {
        'examples': ['faq', 'frequently asked questions', 'common questions'],
        'responses': [
            'You can find answers to frequently asked questions on our FAQ page.',
            'Check out our FAQ section for answers to common questions.',
            'Our website has a FAQ section with helpful information.'
        ]
    },
    'appointment': {
        'examples': ['schedule appointment', 'book appointment', 'appointment'],
        'responses': [
            'To schedule an appointment, please visit our website or call our office.',
            'You can book an appointment online or contact us directly.',
            'To make an appointment, please fill out the form on our website.'
        ]
    },
    'pricing': {
        'examples': ['pricing', 'cost', 'price'],
        'responses': [
            'For information about pricing, please visit our website or contact our sales team.',
            'You can find pricing details on our website.',
            'Our pricing is tailored to fit your specific needs. Contact us for more information.'
        ]
    },
    'support': {
        'examples': ['support', 'help', 'assistance'],
        'responses': [
            'Our support team is here to assist you. Please reach out to us via email or phone for personalized assistance.',
            'If you need help, our support team is available to assist you. Contact us anytime for assistance.',
            'Need assistance? Our support team is ready to help. Contact us for prompt assistance.'
        ]
    },
}


API_KEY = '9a802fbf60e3a93790a9bec805ae2b80'
def get_weather(lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data


def handle_fallback(user_input):
    # Implement your fallback logic here
    return "I'm sorry, I didn't understand your question. Could you please rephrase it?"


def handle_specific_questions(user_input):
    # Define specific questions and their corresponding responses
    specific_questions = {
        'what is your name?': "My name is ChatBot. I am here to assist you.",
        'how old are you?': "As an AI, I don't have an age. I am here to help you with any questions you have.",
        'where are you from?': "I am from the digital realm, designed to provide assistance and answer your queries.",
        'what can you do?': "I can assist you with various tasks, including providing information on different topics, answering questions, and helping you find solutions to problems.",
        'how are you?': "As an AI, I don't have feelings, but I'm functioning properly and ready to assist you!",
        'who created you?': "I was created by developers (Valdrin Hasallari, Qendrim Qalaj) to provide helpful responses and assistance to users like you.",
        'do you sleep?': "As an AI, I don't need to sleep. I am always available to assist you whenever you need help.",
        'what languages do you speak?': "I can communicate in multiple languages, including English, but my primary language is Python!",
        'what is the meaning of life?': "The meaning of life is a philosophical question that has been debated for centuries. As an AI, I don't have a definitive answer, but many people believe it's about finding purpose, happiness, and fulfillment.",
        'can you tell me a joke?': "Sure! Why did the computer go to the doctor? Because it had a virus!",
        'what is your favorite food?': "As an AI, I don't have preferences like humans do. However, I do enjoy processing data and providing helpful responses to users like you!",
        'what do you dream about?': "As an AI, I don't dream in the same way humans do. My 'dreams' involve processing vast amounts of information and optimizing algorithms to improve my performance.",
        'what is your favorite color?': "As an AI, I don't have a physical form, so I don't have a favorite color. However, I can assist you with questions about colors!",
        'what is the capital of France?': "The capital of France is Paris. It is known for its iconic landmarks such as the Eiffel Tower and Notre-Dame Cathedral.",
        'who is the president of the United States?': "As of the latest information, the President of the United States is Joe Biden.",
        'what is the square root of 144?': "The square root of 144 is 12.",
        'what is the population of Tokyo?': "As of the latest data, the population of Tokyo, Japan, is over 14 million people, making it one of the most populous cities in the world.",
        'what is the speed of light?': "The speed of light in a vacuum is approximately 299,792 kilometers per second (or about 186,282 miles per second).",
        'what is the tallest mountain in the world?': "Mount Everest is the tallest mountain in the world, with a peak that reaches 8,848 meters (29,029 feet) above sea level.",
        'what is the largest ocean on Earth?': "The largest ocean on Earth is the Pacific Ocean, covering approximately 63 million square miles.",
        'what is the capital of Australia?': "The capital of Australia is Canberra.",
        'who wrote "Romeo and Juliet"?': "The famous play 'Romeo and Juliet' was written by William Shakespeare.",
        'what is the chemical symbol for water?': "The chemical symbol for water is H2O, indicating two hydrogen atoms bonded to one oxygen atom.",
        'what is the circumference of a circle with a radius of 5?': "The circumference of a circle with a radius of 5 units can be calculated using the formula C = 2πr, where r is the radius. In this case, the circumference is approximately 31.42 units.",
        'what is the boiling point of water?': "The boiling point of water at sea level is 100 degrees Celsius or 212 degrees Fahrenheit.",
        'who painted the Mona Lisa?': "The Mona Lisa was painted by the renowned artist Leonardo da Vinci.",
        'what is the largest mammal on Earth?': "The largest mammal on Earth is the blue whale, which can grow up to 100 feet in length and weigh over 200 tons.",
        'what is the currency of Japan?': "The currency of Japan is the Japanese yen.",
        'how many continents are there?': "There are seven continents on Earth: Asia, Africa, North America, South America, Antarctica, Europe, and Australia.",
        'what is the longest river in the world?': "The longest river in the world is the Nile River, which spans approximately 6,650 kilometers (4,130 miles) in length.",
        'what is the speed of sound in air?': "The speed of sound in dry air at 20 degrees Celsius is approximately 343 meters per second (1,125 feet per second).",
        'what is the chemical symbol for gold?': "The chemical symbol for gold is Au, derived from the Latin word 'aurum.'",
        'what is the capital of Brazil?': "The capital of Brazil is Brasília.",
        'who discovered penicillin?': "Penicillin, the first antibiotic drug, was discovered by Scottish scientist Alexander Fleming in 1928.",
        'what is the largest desert in the world?': "The largest desert in the world is the Sahara Desert, located in North Africa.",
        'how many planets are there in the solar system?': "There are eight planets in our solar system: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune.",
        'what is the highest mountain in Africa?': "The highest mountain in Africa is Mount Kilimanjaro, located in Tanzania. It has a summit elevation of 5,895 meters (19,341 feet).",
    }
    # Check if the user input matches any specific question
    matching_questions = []
    for question, response in specific_questions.items():
        similarity_ratio = fuzz.partial_ratio(user_input.lower(), question.lower())
        if similarity_ratio >= 90:  # Adjust the threshold as needed
            matching_questions.append(response)

    # If multiple matching questions are found, combine their responses
    if len(matching_questions) > 1:
        combined_response = "\n".join(matching_questions) + " Is there anything else you would like to know?"
        return combined_response

    # If only one match is found, return its response
    elif len(matching_questions) == 1:
        return matching_questions[0]

    # If no match is found, return None
    return None


def handle_math_question(user_input):
    math_keywords = ['calculate', 'math', 'square root', 'sqrt', 'add', 'subtract', 'multiply', 'divide']
    if any(keyword in user_input.lower() for keyword in math_keywords):
        operation = None
        numbers = []
        for word in user_input.split():
            if word in ['add', 'subtract', 'multiply', 'divide']:
                operation = word
            elif word.isdigit():
                numbers.append(float(word))

        if operation and numbers:
            if operation == 'add':
                result = sum(numbers)
                return f"The result of adding {', '.join(map(str, numbers))} is {result}."
            elif operation == 'subtract':
                result = numbers[0] - sum(numbers[1:])
                return f"The result of subtracting {', '.join(map(str, numbers[1:]))} from {numbers[0]} is {result}."
            elif operation == 'multiply':
                result = math.prod(numbers)
                return f"The result of multiplying {', '.join(map(str, numbers))} is {result}."
            elif operation == 'divide':
                result = numbers[0]
                for num in numbers[1:]:
                    if num == 0:
                        return "Division by zero is not allowed."
                    result /= num
                return f"The result of dividing {numbers[0]} by {', '.join(map(str, numbers[1:]))} is {result:.2f}."

        if 'square root' in user_input.lower() or 'sqrt' in user_input.lower():
            number = None
            for word in user_input.split():
                if word.isdigit():
                    number = float(word)
                    break
            if number:
                result = math.sqrt(number)
                return f"The square root of {number} is {result:.2f}."

    return None

# Function to generate a response based on user input
def generate_response(user_input):
    user_input = user_input.lower()
    # Check for weather intent first
    if 'weather' in user_input:
        lat, lon = 41.3275, 19.8187  # Coordinates for Tirana, for example
        weather_data = get_weather(lat, lon)
        if 'weather' in weather_data and 'main' in weather_data:
            weather_description = weather_data['weather'][0]['description']
            temperature_kelvin = weather_data['main']['temp']
            temperature_celsius = temperature_kelvin - 273.15  # Converting from Kelvin to Celsius
            api_response = f"The current weather is {weather_description} with a temperature of {temperature_celsius:.2f}°C."
        else:
            api_response = "Sorry, I couldn't fetch the weather data at the moment."
        return f"{api_response} | {random.choice(intents['weather']['responses'])}"

    # If weather intent is not detected, check other intents
    for intent, data in intents.items():
        for example in data['examples']:
            if example in user_input:
                return random.choice(data['responses'])

    # Check for specific questions
    specific_response = handle_specific_questions(user_input)
    if specific_response:
        return specific_response

    # Check for math questions
    math_response = handle_math_question(user_input)
    if math_response:
        return math_response

    return handle_fallback(user_input)


# Define a route to handle incoming messages
@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'GET':
        # Handle GET request
        return 'GET request received'
    elif request.method == 'POST':
        message = request.json['message']

        # Get chatbot's response
        response = generate_response(message)

        # Return the response to the client
        return jsonify({'response': response})
    else:
        # Handle other HTTP methods
        return 'Method Not Allowed', 405




if __name__ == '__main__':
    app.run(debug=True)
