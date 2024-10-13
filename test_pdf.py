# test_data_ingestion.py
import os
import unittest
from pdf_processor import process_pdf
from config import DATA_DIR, PERSIST_DIR

class TestDataIngestion(unittest.TestCase):

    def setUp(self):
        # Create directories for testing if they don't exist
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(PERSIST_DIR, exist_ok=True)

        # Create a dummy PDF file for testing
        self.pdf_path = os.path.join(DATA_DIR, "test_pdf.pdf")
        with open(self.pdf_path, "wb") as f:
            f.write(b"%PDF-1.4 test content")

    def test_process_pdf(self):
        try:
            process_pdf()
            # Check if the index file is created in the PERSIST_DIR
            files = os.listdir(PERSIST_DIR)
            self.assertTrue(any(f.endswith(".json") for f in files))
        except Exception as e:
            self.fail(f"process_pdf raised an exception: {e}")

    def tearDown(self):
        # Clean up: remove the created test files and directories
        if os.path.exists(self.pdf_path):
            os.remove(self.pdf_path)
        for root, dirs, files in os.walk(DATA_DIR):
            for file in files:
                os.remove(os.path.join(root, file))
        for root, dirs, files in os.walk(PERSIST_DIR):
            for file in files:
                os.remove(os.path.join(root, file))

        os.rmdir(DATA_DIR)
        os.rmdir(PERSIST_DIR)

if __name__ == '__main__':
    unittest.main()
