import unittest
from config import HF_TOKEN, LLM_MODEL_NAME, EMBED_MODEL_NAME, PERSIST_DIR, DATA_DIR

class TestConfig(unittest.TestCase):

    def test_env_variables(self):
        self.assertIsNotNone(HF_TOKEN, "HuggingFace token is not set.")
        self.assertEqual(LLM_MODEL_NAME, "google/gemma-1.1-7b-it")
        self.assertEqual(EMBED_MODEL_NAME, "BAAI/bge-small-en-v1.5")
    
    def test_directories(self):
        self.assertEqual(PERSIST_DIR, "./db")
        self.assertEqual(DATA_DIR, "data")

if __name__ == '__main__':
    unittest.main()
