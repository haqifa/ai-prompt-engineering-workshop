import os
import json
from dotenv import load_dotenv
import openai
import requests

load_dotenv()

# --- Currency Converter Tool ---
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Convert currency using exchangerate.host API.
    Supported: any ISO currency code (e.g., USD, EUR, IDR)
    """
    api_key = os.getenv("EXCHANGERATE_API_KEY")
    url = f"https://api.exchangerate.host/convert?from={from_currency.upper()}&to={to_currency.upper()}&amount={amount}"
    if api_key:
        url += f"&access_key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "result" in data and data["result"] is not None:
                result = data["result"]
                return f"{amount} {from_currency.upper()} is equal to {result:.2f} {to_currency.upper()}."
            else:
                return f"Currency conversion failed: {data.get('error', 'Unknown error')}"
        else:
            return f"Currency conversion failed: HTTP {response.status_code}"
    except Exception as e:
        return f"Currency conversion failed: {e}"


# --- Conversion Tools ---
def convert_distance(value: float, from_unit: str, to_unit: str) -> str:
    """
    Convert distance between miles, kilometers, meters, etc.
    Supported units: miles, kilometers (km), meters (m)
    """
    conversions = {
        ("miles", "kilometers"): lambda v: v * 1.60934,
        ("kilometers", "miles"): lambda v: v / 1.60934,
        ("miles", "meters"): lambda v: v * 1609.34,
        ("meters", "miles"): lambda v: v / 1609.34,
        ("kilometers", "meters"): lambda v: v * 1000,
        ("meters", "kilometers"): lambda v: v / 1000,
    }
    key = (from_unit.lower(), to_unit.lower())
    if key in conversions:
        result = conversions[key](value)
        return f"{value} {from_unit} is equal to {result:.2f} {to_unit}."
    else:
        return f"Conversion from {from_unit} to {to_unit} is not supported."

def convert_weight(value: float, from_unit: str, to_unit: str) -> str:
    """
    Convert weight between kilograms and pounds.
    Supported units: kilograms (kg), pounds (lbs)
    """
    conversions = {
        ("kilograms", "pounds"): lambda v: v * 2.20462,
        ("pounds", "kilograms"): lambda v: v / 2.20462,
    }
    key = (from_unit.lower(), to_unit.lower())
    if key in conversions:
        result = conversions[key](value)
        return f"{value} {from_unit} is equal to {result:.2f} {to_unit}."
    else:
        return f"Conversion from {from_unit} to {to_unit} is not supported."

# Get the API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Weather API key
WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
MODEL = "gpt-3.5-turbo"
def get_weather(city: str) -> str:
    """
    Get the weather for a city.
    :param city: The city to get the weather for.
    :return: The weather for the city.
    """
    # Not a real API key, just a placeholder
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return json.dumps(
            {
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"].get("humidity"),
                "wind_speed": data["wind"].get("speed"),
                "city": data.get("name"),
                "country": data["sys"].get("country"),
            }
        )
    else:
        return json.dumps({"error": "Could not get weather"})


def run_conversation(user_input: str):
    # Step 1: send the conversation and available functions to GPT
    system_prompt = (
        "You are an advanced personal assistant.\n"
        "You have access to the following tools: get_weather, convert_distance, convert_weight.\n"
        "- get_weather(city: string): Returns the current weather for a city, including temperature, description, humidity, wind speed, city, and country.\n"
        "- convert_distance(value: float, from_unit: string, to_unit: string): Converts distance between miles, kilometers, and meters.\n"
        "- convert_weight(value: float, from_unit: string, to_unit: string): Converts weight between kilograms and pounds.\n"
        "Whenever you use get_weather, you must always analyze the weather result and provide a practical clothing suggestion in your final answer.\n"
        "Clothing advice must be based on temperature, weather description, humidity, and wind speed.\n"
        "For example:\n"
        "- If it is sunny and 24°C, say: 'It's a warm and pleasant day, so I'd recommend wearing a t-shirt and shorts. Don't forget your sunglasses!'\n"
        "- If it is rainy and 15°C, say: 'It's cool and rainy, so bring a light jacket and an umbrella.'\n"
        "- If it is cold (below 10°C), say: 'It's cold, so wear a warm coat, scarf, and gloves.'\n"
        "- If it is windy, mention windbreakers or secure hats.\n"
        "For conversion tools, always answer with the converted value in a clear sentence.\n"
    )
def run_conversation(user_input: str, candidate_instruction: str = None):
    base_prompt = (
        "You are an advanced personal assistant.\n"
        "You have access to the following tools: get_weather, convert_distance, convert_weight, convert_currency.\n"
        "- get_weather(city: string): Returns the current weather for a city, including temperature, description, humidity, wind speed, city, and country.\n"
        "- convert_distance(value: float, from_unit: string, to_unit: string): Converts distance between miles, kilometers, and meters.\n"
        "- convert_weight(value: float, from_unit: string, to_unit: string): Converts weight between kilograms and pounds.\n"
        "- convert_currency(amount: float, from_currency: string, to_currency: string): Converts currency using live exchange rates.\n"
    )
    # Only add fashion advice rules for B and C
    if candidate_instruction and ("outfit recommendation" in candidate_instruction or "fashion advice" in candidate_instruction):
        fashion_rules = (
            "Whenever you use get_weather, you must always analyze the weather result and provide a practical clothing suggestion in your final answer.\n"
            "Clothing advice must be based on temperature, weather description, humidity, and wind speed.\n"
            "For example:\n"
            "- If it is sunny and 24°C, say: 'It's a warm and pleasant day, so I'd recommend wearing a t-shirt and shorts. Don't forget your sunglasses!'\n"
            "- If it is rainy and 15°C, say: 'It's cool and rainy, so bring a light jacket and an umbrella.'\n"
            "- If it is cold (below 10°C), say: 'It's cold, so wear a warm coat, scarf, and gloves.'\n"
            "- If it is windy, mention windbreakers or secure hats.\n"
        )
        system_prompt = base_prompt + "\n" + fashion_rules + "\n" + candidate_instruction
    else:
        system_prompt = base_prompt + ("\n" + candidate_instruction if candidate_instruction else "")
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]
    functions = [
        {
            "name": "get_weather",
            "description": "Get the current weather in a given city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                },
                "required": ["city"],
            },
        },
        {
            "name": "convert_currency",
            "description": "Convert currency using live exchange rates. Arguments: amount (float), from_currency (string), to_currency (string).",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number", "description": "The amount to convert."},
                    "from_currency": {"type": "string", "description": "The currency code to convert from (e.g., USD, EUR, IDR)."},
                    "to_currency": {"type": "string", "description": "The currency code to convert to (e.g., USD, EUR, IDR)."},
                },
                "required": ["amount", "from_currency", "to_currency"],
            },
        },
        {
            "name": "convert_distance",
            "description": "Convert distance between miles, kilometers, and meters. Arguments: value (float), from_unit (string), to_unit (string).",
            "parameters": {
                "type": "object",
                "properties": {
                    "value": {"type": "number", "description": "The numeric value to convert."},
                    "from_unit": {"type": "string", "description": "The unit to convert from (e.g., miles, kilometers, meters)."},
                    "to_unit": {"type": "string", "description": "The unit to convert to (e.g., miles, kilometers, meters)."},
                },
                "required": ["value", "from_unit", "to_unit"],
            },
        },
        {
            "name": "convert_weight",
            "description": "Convert weight between kilograms and pounds. Arguments: value (float), from_unit (string), to_unit (string).",
            "parameters": {
                "type": "object",
                "properties": {
                    "value": {"type": "number", "description": "The numeric value to convert."},
                    "from_unit": {"type": "string", "description": "The unit to convert from (e.g., kilograms, pounds)."},
                    "to_unit": {"type": "string", "description": "The unit to convert to (e.g., kilograms, pounds)."},
                },
                "required": ["value", "from_unit", "to_unit"],
            },
        },
    ]
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_weather": get_weather,
            "convert_distance": convert_distance,
            "convert_weight": convert_weight,
            "convert_currency": convert_currency,
        }
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        # Dynamically call the function with all arguments
        function_response = function_to_call(**function_args)

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )
        second_response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
        )
        return second_response
    return response


def select_prompt_candidate():
    print("Select prompt candidate:")
    print("A. Simple")
    print("B. Detailed")
    print("C. Chain-of-Thought")
    while True:
        choice = input("Enter A, B, or C: ").strip().upper()
        if choice == "A":
            return "You must select the correct tool to answer the user's request. After using a tool, present the information clearly."
        elif choice == "B":
            return ("Carefully analyze the user's request to choose the right tool. Crucially, if you use the get_weather tool, you must also provide a helpful outfit recommendation in your final answer. For all other tools, just state the result.")
        elif choice == "C":
            return ("Think step-by-step to solve the user's request. First, identify the user's goal. Second, select the best tool. Third, execute the tool. Finally, formulate the final answer. Remember the special rule: always add fashion advice after reporting the weather.")
        else:
            print("Invalid input. Please enter A, B, or C.")

if __name__ == "__main__":
    while True:
        candidate_instruction = select_prompt_candidate()
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = run_conversation(user_input, candidate_instruction)
        print(f"AI: {response.choices[0].message.content}")
