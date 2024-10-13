# config.py
import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

# Llama index settings
LLM_MODEL_NAME = "google/gemma-1.1-7b-it"
EMBED_MODEL_NAME = "BAAI/bge-small-en-v1.5"
PERSIST_DIR = "./db"
DATA_DIR = "data"
