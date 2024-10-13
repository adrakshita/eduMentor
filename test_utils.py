import base64
import unittest
from unittest.mock import patch, mock_open
from utils import display_pdf

class TestUtils(unittest.TestCase):

    @patch('utils.st.markdown')
    @patch('builtins.open', new_callable=mock_open, read_data=b'%PDF-1.4\n%...')
    def test_display_pdf(self, mock_open, mock_markdown):
        # Define the file path to use in the test
        file_path = 'path/to/test.pdf'
        
        # Call the function to test
        display_pdf(file_path)
        
        # Read the base64 encoded PDF from the mock file
        mock_open.assert_called_once_with(file_path, "rb")
        base64_pdf = mock_open().read()
        base64_encoded = base64.b64encode(base64_pdf).decode('utf-8')
        
        # Check that st.markdown was called with the expected arguments
        expected_pdf_display = f'<iframe src="data:application/pdf;base64,{base64_encoded}" width="100%" height="600" type="application/pdf"></iframe>'
        mock_markdown.assert_called_once_with(expected_pdf_display, unsafe_allow_html=True)

if __name__ == '__main__':
    unittest.main()
