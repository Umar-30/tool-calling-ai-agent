import asyncio
import json
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from tools import tools_schema, function_map

# 1. Configuration & Settings
load_dotenv()

class Settings:
    @classmethod
    def get_api_key(cls):
        return os.getenv("COHERE_API_KEY")

    BASE_URL = "https://api.cohere.com/compatibility/v1"
    MODEL_NAME = "command-r-08-2024"

# 2. Agent Logic
async def run_agent(user_input: str):
    api_key = Settings.get_api_key()
    if not api_key:
        return {"status": "error", "message": "COHERE_API_KEY is missing. Please set it in Secrets or .env"}

    client = AsyncOpenAI(
        api_key=api_key,
        base_url=Settings.BASE_URL,
    )
    
    messages = [{"role": "user", "content": user_input}]

    try:
        for _ in range(5):
            response = await client.chat.completions.create(
                model=Settings.MODEL_NAME,
                messages=messages,
                tools=tools_schema,
                tool_choice="auto"
            )

            message = response.choices[0].message

            # Handle Tool Calls
            if message.tool_calls:
                messages.append(message)
                for tool_call in message.tool_calls:
                    name = tool_call.function.name
                    
                    # Error Handling: Tool existence
                    if name not in function_map:
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps({"error": f"Tool '{name}' not found"})
                        })
                        continue

                    # Error Handling: Execution safety
                    try:
                        args = json.loads(tool_call.function.arguments)
                        result = function_map[name](**args)
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(result)
                        })
                    except Exception as e:
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps({"error": str(e)})
                        })
                continue

            # Return Success JSON
            return {
                "status": "success",
                "response": message.content or "No response generated."
            }

        return {"status": "error", "message": "Max iterations reached"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# 3. Main Loop
async def main():
    print("--- Tool-Calling AI Agent (Cohere) ---")
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                break
            if not user_input:
                continue

            result = await run_agent(user_input)
            print("Agent:", json.dumps(result, indent=2))
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    asyncio.run(main())
