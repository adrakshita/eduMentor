import streamlit as st
from pdf_handler import handle_pdf_upload
from query_handler import handle_query
from chat_manager import create_chat, select_chat, delete_chat
from config import PERSIST_DIR, HF_TOKEN, LLM_MODEL_NAME, EMBED_MODEL_NAME
from llama_index.llms.huggingface import HuggingFaceInferenceAPI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings


# Initialize settings
def initialize_settings():
    # Setting up the LLM and embeddings using Hugging Face Inference API
    Settings.llm = HuggingFaceInferenceAPI(
        model_name=LLM_MODEL_NAME,
        tokenizer_name=LLM_MODEL_NAME,
        context_window=3000,
        token=HF_TOKEN,
        max_new_tokens=512,
        generate_kwargs={"temperature": 0.1},
    )
    Settings.embed_model = HuggingFaceEmbedding(
        model_name=EMBED_MODEL_NAME
    )

initialize_settings()

# Initialize session state for chats
if 'chats' not in st.session_state:
    st.session_state.chats = {}
    st.session_state.current_chat = None

def handle_sidebar_action():
    # Sidebar for chat management
    with st.sidebar:
        st.title("Chat Management")
        
        chat_action = st.selectbox("Choose an action", ["Create Chat", "Select Chat", "Delete Chat"])
        
        if chat_action == "Create Chat":
            chat_name = st.text_input("Enter chat name")
            if chat_name:
                create_chat(chat_name)
    
        elif chat_action == "Select Chat":
            chat_name = st.selectbox("Select chat", list(st.session_state.chats.keys()))
            if chat_name:
                select_chat(chat_name)
    
        elif chat_action == "Delete Chat":
            chat_name = st.selectbox("Select chat to delete", list(st.session_state.chats.keys()))
            if chat_name:
                delete_chat(chat_name)

def main_app_interface():
    # Main app interface
    st.title("Edu Mentor-an AI Tutor")
    st.markdown("Retrieval-Augmented Generation") 
    st.markdown("Start a chat...🚀")

    if st.session_state.current_chat:
        handle_pdf_upload()

        user_prompt = st.chat_input("Ask me anything about the content of the PDF:")
        if user_prompt:
            st.session_state.chats[st.session_state.current_chat].append({'role': 'user', "content": user_prompt})
            response = handle_query(user_prompt)
            st.session_state.chats[st.session_state.current_chat].append({'role': 'assistant', "content": response})

        for message in st.session_state.chats.get(st.session_state.current_chat, []):
            with st.chat_message(message['role']):
                st.write(message['content'])
    else:
        st.warning("Please create or select a chat to start.")

    

def run_app():
    handle_sidebar_action()
    main_app_interface()

# Entry point for Streamlit app
if __name__ == "__main__":
    run_app()
