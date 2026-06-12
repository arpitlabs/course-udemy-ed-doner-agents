import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")

# Define tools/functions
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the weather for a specific location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit",
                    },
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform basic arithmetic calculations",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "The arithmetic operation",
                    },
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["operation", "a", "b"],
            },
        },
    },
]


def get_weather(location: str, unit: str = "fahrenheit") -> str:
    """Simulate weather API call"""
    return f"Weather in {location}: 72°{unit[0].upper()}, Sunny"


def calculate(operation: str, a: float, b: float) -> float:
    """Perform calculations"""
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else None,
    }
    return operations[operation](a, b)


def process_tool_call(tool_name: str, tool_input: dict):
    """Execute the appropriate function based on tool call"""
    if tool_name == "get_weather":
        return get_weather(**tool_input)
    elif tool_name == "calculate":
        return calculate(**tool_input)
    else:
        return f"Unknown tool: {tool_name}"


def main():
    messages = [
        {
            "role": "user",
            "content": "What is the weather in New York and what is 15 * 8?",
        }
    ]

    print("User: What is the weather in New York and what is 15 * 8?\n")

    # Make initial request
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    # Process tool calls in a loop
    while response.choices[0].finish_reason == "tool_calls":
        tool_calls = response.choices[0].message.tool_calls
        messages.append({"role": "assistant", "content": "", "tool_calls": tool_calls})

        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_input = json.loads(tool_call.function.arguments)
            result = process_tool_call(tool_name, tool_input)

            print(f"Function called: {tool_name}")
            print(f"Parameters: {tool_input}")
            print(f"Result: {result}\n")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": str(result),
                }
            )

        # Make follow-up request
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

    # Print final response
    final_response = response.choices[0].message.content
    print(f"Assistant: {final_response}")


if __name__ == "__main__":
    main()
