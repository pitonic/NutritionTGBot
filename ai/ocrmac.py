import streamlit as st
import requests
import base64
from PIL import Image
import os
import tempfile  # Add this import

from ocrmac import ocrmac

# Define the URL for the local LLaMA 3.2 API
LLAMA_API_URL = "http://ollama:11434/api/generate"

def ocr_mac_demo(image_file):

    annotations = ocrmac.OCR('test.png').recognize()
    return annotations




def main():
    st.title("ocr_mac_demo Image Analysis")
    st.write("Upload an image to ocr it.")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp", "heic", "heif"])

    if uploaded_file is not None:
        st.write("### Uploaded Image")
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)

        st.write("### Processing Image...")
        response = ocr_mac_demo(image)

        if response:
            st.write("### OCR.MAC API Response")
            st.write(response)
        else:
            st.error("Failed to get a response from ocr")

if __name__ == "__main__":
    main()
