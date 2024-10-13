# test_query_handler.py
import unittest
from unittest.mock import patch, MagicMock
from query_handler import handle_query

class TestQueryHandler(unittest.TestCase):

    @patch('query_handler.load_index_from_storage')
    @patch('query_handler.StorageContext.from_defaults')
    @patch('query_handler.ChatPromptTemplate.from_messages')
    def test_handle_query(self, mock_chat_prompt_template, mock_storage_context, mock_load_index):
        # Setup mocks
        mock_storage_context.return_value = MagicMock()
        mock_index = MagicMock()
        mock_load_index.return_value = mock_index

        mock_query_engine = MagicMock()
        mock_index.as_query_engine.return_value = mock_query_engine

        # Define the mock response
        mock_query_engine.query.return_value = MagicMock(response="This is a mocked response.")

        # Define the input query
        query = "What is the purpose of this chatbot?"

        # Call the function to test
        result = handle_query(query)

        # Assert that the result is as expected
        self.assertEqual(result, "This is a mocked response.")

        # Assert that the correct methods were called
        mock_storage_context.assert_called_once_with(persist_dir='./db')
        mock_load_index.assert_called_once_with(mock_storage_context.return_value)
        mock_index.as_query_engine.assert_called_once_with(text_qa_template=mock_chat_prompt_template.return_value)
        mock_query_engine.query.assert_called_once_with(query)

    @patch('query_handler.load_index_from_storage')
    @patch('query_handler.StorageContext.from_defaults')
    @patch('query_handler.ChatPromptTemplate.from_messages')
    def test_handle_query_no_response(self, mock_chat_prompt_template, mock_storage_context, mock_load_index):
        # Setup mocks
        mock_storage_context.return_value = MagicMock()
        mock_index = MagicMock()
        mock_load_index.return_value = mock_index

        mock_query_engine = MagicMock()
        mock_index.as_query_engine.return_value = mock_query_engine

        # Define the mock response without 'response'
        mock_query_engine.query.return_value = "No response"

        # Define the input query
        query = "What is the purpose of this chatbot?"

        # Call the function to test
        result = handle_query(query)

        # Assert that the result is as expected
        self.assertEqual(result, "Sorry, I couldn't find an answer.")

        # Assert that the correct methods were called
        mock_storage_context.assert_called_once_with(persist_dir='./db')
        mock_load_index.assert_called_once_with(mock_storage_context.return_value)
        mock_index.as_query_engine.assert_called_once_with(text_qa_template=mock_chat_prompt_template.return_value)
        mock_query_engine.query.assert_called_once_with(query)

if __name__ == '__main__':
    unittest.main()
