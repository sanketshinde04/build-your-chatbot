import streamlit as st
from google import genai

# Helper function to extract text safely from Gemini response
def extract_text_from_response(response):
    """Extract text content from Gemini response, ignoring non-text parts like thought_signature"""
    text_parts = []
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'text'):
            text_parts.append(part.text)
    return "".join(text_parts) if text_parts else ""

# Page config
st.set_page_config(page_title="Gemini Chatbot", page_icon="💬")

# Header
st.title("💬 Gemini Chatbot")
st.caption("A simple chatbot powered by Google's Gemini model")

# Initialize Gemini client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

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

    # Create chat and replay history
    chat = client.chats.create(model="gemini-3.1-flash-lite-preview")
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

# Sidebar
st.sidebar.title("About")
st.sidebar.info("This chatbot uses Google's gemini-3.1-flash-lite-preview model to have conversations with you.")
st.sidebar.markdown("---")
st.sidebar.markdown("❤️ Made by [Build Fast with AI](https://buildfastwithai.com)")
