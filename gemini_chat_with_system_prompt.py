import streamlit as st
from google import genai
from google.genai import types

# Helper function to extract text safely from Gemini response
def extract_text_from_response(response):
    """Extract text content from Gemini response, ignoring non-text parts like thought_signature"""
    text_parts = []
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'text'):
            text_parts.append(part.text)
    return "".join(text_parts) if text_parts else ""

# Page config
st.set_page_config(page_title="Gemini Chatbot with System Prompt", page_icon="💬")

# Header
st.title("💬 Gemini Chatbot")
st.caption("Customize the chatbot's behavior using the system prompt in the sidebar")

# Initialize Gemini client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Sidebar for system prompt
st.sidebar.title("⚙️ Custom Instructions")
st.sidebar.write("Modify the system prompt below to change how the chatbot responds.")

system_prompt = st.sidebar.text_area(
    "System Prompt",
    value="You are a helpful assistant.",
    height=150,
    help="The system prompt sets the behavior and personality of the AI assistant."
)

st.sidebar.info("💡 **Tip:** Try prompts like:\n- 'You are a friendly pirate'\n- 'Respond only in haikus'\n- 'You are a coding tutor'")

# Reset chat when system prompt changes
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = system_prompt
    st.session_state.history = []

if st.session_state.system_prompt != system_prompt:
    st.session_state.system_prompt = system_prompt
    st.session_state.history = []
    st.rerun()

# Display chat history
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Create chat with system prompt
    chat = client.chats.create(
        model="gemini-3.1-flash-lite-preview",
        config=types.GenerateContentConfig(system_instruction=system_prompt)
    )
    
    # Replay previous messages
    for msg in st.session_state.history[:-1]:
        if msg["role"] == "user":
            chat.send_message(msg["content"])

    # Get response from Gemini
    with st.chat_message("assistant"):
        response = chat.send_message(prompt)
        reply = extract_text_from_response(response)
        st.markdown(reply)

    # Add assistant message to history
    st.session_state.history.append({"role": "assistant", "content": reply})

st.sidebar.markdown("---")
st.sidebar.markdown("❤️ Made by [Build Fast with AI](https://buildfastwithai.com)")
