# pdf_processor.py
from llama_index.core import StorageContext, VectorStoreIndex, SimpleDirectoryReader
from config import DATA_DIR, PERSIST_DIR

def process_pdf():
    documents = SimpleDirectoryReader(DATA_DIR).load_data()
    storage_context = StorageContext.from_defaults()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
