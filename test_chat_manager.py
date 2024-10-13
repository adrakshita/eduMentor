import unittest
import streamlit as st
from chat_manager import create_chat, select_chat, delete_chat

class TestChatManager(unittest.TestCase):

    def setUp(self):
        st.session_state.clear()
        st.session_state.chats = {}
        st.session_state.current_chat = None

    def test_create_chat(self):
        create_chat("TestChat")
        self.assertIn("TestChat", st.session_state.chats)

    def test_select_chat(self):
        st.session_state.chats["TestChat"] = []
        select_chat("TestChat")
        self.assertEqual(st.session_state.current_chat, "TestChat")

    def test_delete_chat(self):
        st.session_state.chats["TestChat"] = []
        delete_chat("TestChat")
        self.assertNotIn("TestChat", st.session_state.chats)

if __name__ == '__main__':
    unittest.main()
