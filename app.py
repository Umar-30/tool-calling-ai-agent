import streamlit as st
import asyncio
import json
from main import run_agent

# Page Configuration
st.set_page_config(
    page_title="Tool-Calling AI Agent",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for a better look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
    }
    .sidebar .sidebar-content {
        background-color: #e9ecef;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #dee2e6;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar - Project Info
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
    st.title("🤖 AI Assistant")
    st.markdown("---")
    
    st.info("""
    **About this Agent:**
    This is a smart AI assistant 🤖 that uses tools 🛠️ to help you. 
    It can check the weather 🌤️, solve math problems ➕, and more!
    """)
    
    st.markdown("### ⚙️ Configuration")
    st.write(f"**Model:** `command-r-08-2024` 🧠")
    st.write(f"**Provider:** `Cohere` ☁️")
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Main Header
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/2040/2040946.png", width=80)
with col2:
    st.title("Tool-Calling AI Agent")
    st.caption("🚀 Intelligent automation powered by Cohere")

st.markdown("---")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            # Show JSON in an expander
            if "raw_response" in message:
                with st.expander("🔍 View Technical Details (JSON)"):
                    st.json(message["raw_response"])
            st.markdown(message["content"])
        else:
            st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask me something (e.g., 'What is 156 + 244?')"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Agent Response
    with st.chat_message("assistant"):
        with st.status("🤖 Agent is thinking...", expanded=True) as status:
            st.write("Checking tools...")
            # Run the agent logic
            result = asyncio.run(run_agent(prompt))
            
            if result["status"] == "success":
                st.write("Tool call completed!")
                response_text = result["response"]
                
                with st.expander("🔍 View Technical Details (JSON)"):
                    st.json(result)
                
                st.markdown(response_text)
                
                # Add to history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response_text,
                    "status": "success",
                    "raw_response": result
                })
                status.update(label="✅ Response Ready!", state="complete", expanded=False)
            else:
                error_msg = f"❌ Error: {result.get('message', 'Unknown error')}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                status.update(label="❌ Execution Failed", state="error")
