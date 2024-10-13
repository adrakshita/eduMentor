# pdf_handler.py
import os
import streamlit as st
from config import DATA_DIR, PERSIST_DIR

def handle_pdf_upload():
    # Ensure the DATA_DIR exists
    os.makedirs(DATA_DIR, exist_ok=True)

    uploaded_file = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button")
    if st.button("Submit & Process"):
        if uploaded_file is not None:
            filepath = os.path.join(DATA_DIR, "saved_pdf.pdf")
            with open(filepath, "wb") as f:
                f.write(uploaded_file.getbuffer())
            # Import process_pdf here to avoid circular import issues
            from pdf_processor import process_pdf
            process_pdf()  # Process PDF every time a new file is uploaded
            st.success("Done")
        else:
            st.warning("Please upload a PDF file.")
