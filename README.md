# Smarter AI Assistant: Workshop Project

Welcome to the Hands-On Workshop: Building and Evaluating a Smarter AI!

This project demonstrates how to upgrade a basic AI bot into a multi-talented assistant using modern prompt engineering techniques. The focus is on expanding the assistant's reasoning ability and tool usage to deliver more helpful, context-aware responses.

---

## Overview

The upgraded AI assistant is designed to:

- **Fashion Advisor:** Not only report the weather, but also recommend suitable outfits based on the conditions.
- **Universal Converter:** Convert currencies using the latest exchange rates.

The assistant utilizes the following tools:
- `get_weather(city: string)`: Provides current weather data for the specified city.
- `convert_currency(amount: float, from: string, to: string)`: Converts specified currency amounts.

---

## Prompt Engineering Approach

To optimize the assistant's capabilities, several prompt strategies were explored:

1. **Simple Prompt:** Direct instructions for tool usage and clear information presentation.
2. **Detailed Prompt:** Specific guidance to provide fashion advice when reporting the weather.
3. **Chain-of-Thought Prompt:** Step-by-step reasoning to improve decision-making and ensure fashion advice is included with weather reports.

Each prompt is plugged into the following template:

```
You are a helpful AI assistant. You have access to the following tools:
- get_weather(city: string)
- convert_currency(amount: float, from: string, to: string)

{instruction_variant}

Answer the user's question.
```

---

## Sample Dataset

To showcase the assistant's capabilities, here are example user questions and ideal answers:

| User Input                        | Ideal Answer                                                                |
|------------------------------------|----------------------------------------------------------------------------|
| What's the weather like in Bandung?| The weather in Bandung is 24°C and Sunny. It's a warm day, so I'd recommend a t-shirt and shorts. |
| How much is 50 USD in IDR?        | 50 USD is equal to 820,000 IDR.                                             |
| Is it cold in London?              | The weather in London is 15°C with Light Rain. It's a bit chilly, so you should wear a jacket and bring an umbrella. |

---

## How It Works

- The assistant receives a user question.
- It selects the appropriate tool to fetch weather or currency data.
- When providing weather information, it adds helpful outfit recommendations.
- For currency queries, it reports the conversion result directly.

---

## Getting Started

To implement your own version:

1. Integrate weather and currency conversion APIs.
2. Use prompt engineering to guide the AI's tool selection and answer formulation.
3. Customize prompts for your specific needs and test on diverse user questions.

---

## Project Goals

- Demonstrate prompt engineering for enhanced AI reasoning.
- Show how to combine multiple tools for richer user assistance.
- Provide clear documentation and examples for future extension.

---

## License

This project is for educational and demonstration purposes.
