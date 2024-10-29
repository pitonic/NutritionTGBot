import streamlit as st
import requests
import base64
from PIL import Image
import os
import tempfile  # Add this import

# Define the URL for the local LLaMA 3.2 API
LLAMA_API_URL = "http://ollama:11434/api/generate"

def encode_image_to_base64(image_file):
    """
    Encode the uploaded image to a base64 string.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=image_file.name.split('.')[-1]) as temp_file:
        temp_file.write(image_file.getbuffer())
        temp_file_path = temp_file.name

    with open(temp_file_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Clean up the temporary file
    os.remove(temp_file_path)

    return image_data

def send_to_llama_api(image_data):
    """
    Send the base64 encoded image to the LLaMA API and return the response.
    """
    payload = {
        "model": "minicpm-v",
        "prompt": "extract all text from the image",
        "stream": False,
        "images": [image_data]  # Ensure this contains the base64 string
    }

    # Debugging: Print the payload
    st.write("Payload sent to LLaMA API:", payload)

    try:
        response = requests.post(LLAMA_API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to LLaMA API: {e}")
        return None

def main():
    st.title("LLaMA API Image Analysis")
    st.write("Upload an image to analyze it.")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp", "heic", "heif"])

    if uploaded_file is not None:
        st.write("### Uploaded Image")
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)

        st.write("### Processing Image...")
        image_data = encode_image_to_base64(uploaded_file)  # Encode the image
        response = send_to_llama_api(image_data)  # Send to LLaMA API

        if response:
            st.write("### LLaMA API Response")
            st.json(response)  # Display API response as JSON
        else:
            st.error("Failed to get a response from the LLaMA API.")

if __name__ == "__main__":
    main()
