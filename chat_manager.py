import streamlit as st

def create_chat(chat_name):
    if 'chats' not in st.session_state:
        st.session_state.chats = {}
    st.session_state.chats[chat_name] = []

def select_chat(chat_name):
    if chat_name in st.session_state.chats:
        st.session_state.current_chat = chat_name

def delete_chat(chat_name):
    if chat_name in st.session_state.chats:
        del st.session_state.chats[chat_name]
