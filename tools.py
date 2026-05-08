def get_weather(city: str):
    """Get weather for a specific city."""
    return {
        "city": city,
        "temp": "33°C",
        "condition": "Sunny"
    }


def add_numbers(a: float, b: float):
    """Add two numbers."""
    return {"result": a + b}

# Consolidated Schemas
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a specific city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_numbers",
            "description": "Add two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        }
    }
]

# Function Map for easy execution
function_map = {
    "get_weather": get_weather,
    "add_numbers": add_numbers
}
