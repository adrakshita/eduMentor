import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
import app

class TestApp(unittest.TestCase):

    def setUp(self):
        # Clear session state before each test
        st.session_state.clear()
        st.session_state.chats = {}
        st.session_state.current_chat = None

    @patch('app.create_chat')
    @patch('app.select_chat')
    @patch('app.delete_chat')
    def test_sidebar_actions(self, mock_delete_chat, mock_select_chat, mock_create_chat):
        # Simulate the sidebar action for creating a chat
        with patch('streamlit.sidebar.selectbox', return_value='Create Chat'):
            with patch('streamlit.sidebar.text_input', return_value='TestChat'):
                app.handle_sidebar_action()
                mock_create_chat.assert_called_once_with('TestChat')

        # Simulate the sidebar action for selecting a chat
        with patch('streamlit.sidebar.selectbox', return_value='Select Chat'):
            st.session_state.chats['TestChat'] = []
            st.session_state.current_chat = 'TestChat'
            app.handle_sidebar_action()
            mock_select_chat.assert_called_once_with('TestChat')

        # Simulate the sidebar action for deleting a chat
        with patch('streamlit.sidebar.selectbox', return_value='Delete Chat'):
            st.session_state.chats['TestChat'] = []
            with patch('streamlit.sidebar.selectbox', return_value='TestChat'):
                app.handle_sidebar_action()
                mock_delete_chat.assert_called_once_with('TestChat')

    @patch('app.handle_pdf_upload')
    @patch('app.handle_query')
    def test_main_app_interface(self, mock_handle_query, mock_handle_pdf_upload):
        # Set the session state to have a current chat
        st.session_state.current_chat = 'TestChat'
        st.session_state.chats['TestChat'] = []

        mock_handle_pdf_upload.return_value = None
        mock_handle_query.return_value = "Test Response"

        # Simulate user input and processing
        with patch('streamlit.chat_input', return_value='Test question'):
            app.main_app_interface()
            mock_handle_query.assert_called_once_with('Test question')

        # Ensure response is processed and added to chat
        self.assertIn({'role': 'user', 'content': 'Test question'}, st.session_state.chats['TestChat'])
        self.assertIn({'role': 'assistant', 'content': 'Test Response'}, st.session_state.chats['TestChat'])

    def test_initialize_settings(self):
        # Test if the settings are initialized correctly
        app.initialize_settings()
        self.assertIsNotNone(app.Settings.llm)
        self.assertIsNotNone(app.Settings.embed_model)

if __name__ == '__main__':
    unittest.main()
