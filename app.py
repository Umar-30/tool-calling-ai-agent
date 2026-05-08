import streamlit as st
import asyncio
import json
from main import run_agent

# Page Configuration
st.set_page_config(
    page_title="Tool-Calling AI Agent",
    page_icon="🤖",
    layout="centered"
)

# Sidebar - Project Info
with st.sidebar:
    st.title("🤖 AI Agent")
    st.markdown("---")
    st.markdown("**Model:** `command-r-08-2024`")
    st.markdown("**Provider:** Cohere")
    st.markdown("---")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Title
st.title("Tool-Calling AI Agent")
st.caption("Ask me about the weather or simple math!")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            # Show JSON status if available
            if "status" in message:
                st.json(message["raw_response"])
            st.markdown(message["content"])
        else:
            st.markdown(message["content"])

# User Input
if prompt := st.chat_input("What is 156 + 244?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Agent Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Run the agent logic
            result = asyncio.run(run_agent(prompt))
            
            if result["status"] == "success":
                response_text = result["response"]
                # Display JSON
                st.json(result)
                st.markdown(response_text)
                
                # Add to history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response_text,
                    "status": "success",
                    "raw_response": result
                })
            else:
                error_msg = f"Error: {result.get('message', 'Unknown error')}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
