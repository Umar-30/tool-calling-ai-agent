# Tool-Calling AI Agent (Cohere)

A robust, lightweight AI Agent built with Python that demonstrates advanced **Function Calling**, structured **JSON Responses**, and comprehensive **Error Handling** using the Cohere API (via OpenAI compatibility).

## 🚀 Features

-   **Function Calling:** The agent can intelligently decide when to use local tools (like weather lookup or math) to answer user queries.
-   **Multi-Turn Logic:** Supports multiple tool calls in a single response.
-   **JSON Responses:** Every interaction is returned in a clean, structured JSON format.
-   **Error Handling:** Gracefully handles API issues, tool execution failures, and invalid model requests.
-   **Optimized Performance:** Uses Cohere's `command-r-08-2024` model for fast and reliable performance.

## 🛠️ Project Structure

The project has been simplified into just two core files:

-   `main.py`: Contains the core agent logic, configuration, and interactive CLI.
-   `tools.py`: Contains the tool functions and their corresponding JSON schemas.

## 📋 Prerequisites

-   Python 3.14+
-   [uv](https://github.com/astral-sh/uv) (recommended for package management)
-   Cohere API Key

## ⚙️ Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd tool-calling-ai-agent
    ```

2.  **Install dependencies:**
    ```bash
    uv pip install openai-agents python-dotenv
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file in the root directory and add your Cohere API key:
    ```env
    COHERE_API_KEY=your_cohere_api_key_here
    ```

## 🎮 Usage

### 1. Interactive CLI:
```bash
uv run main.py
```

### 2. Streamlit Web UI:
```bash
uv run streamlit run app.py
```

### Example Queries:
-   *"What is the weather in Karachi today?"*
-   *"What is 156 + 244?"*
-   *"Add 5 and 10, then tell me the weather in London."* (Combined tools)

## 📊 Example Output

When you ask a question, the agent responds with a structured JSON:

```json
{
  "status": "success",
  "response": "The sum of 156 and 244 is 400. Currently, the weather in Karachi is 33°C and sunny."
}
```

In case of an error:
```json
{
  "status": "error",
  "message": "Tool 'book_flight' not found"
}
```

## 🛠️ Adding New Tools

To add a new tool:
1.  Define the function in `tools.py`.
2.  Add its JSON schema to `tools_schema` in `tools.py`.
3.  Add the function to the `function_map` in `tools.py`.

---
Developed as part of a Beginner AI Agent Internship project.
