import streamlit as st
import requests
import base64
from PIL import Image
import io

# Define the URL for the local LLaMA 3.2 API
LLAMA_API_URL = "http://ollama:11434/api/generate"

def encode_image_to_base64(image_file):
    """
    Encode the uploaded image to a base64 string.
    """
    # Read image data directly and encode to base64
    image_data = image_file.read()
    return base64.b64encode(image_data).decode('utf-8')

def send_to_llama_api(b64image_data):
    """
    Send the base64 encoded image to the LLaMA API and return the response.
    """
    payload = {
        "model": "llava-llama3",
        "prompt": "What is in this picture?",
        "stream": False,
        "images": [b64image_data]  # Ensure this contains the base64 string
    }
    st.write("image-b64:", b64image_data)
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

    # File uploader for image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp", "heic", "heif"])

    if uploaded_file is not None:
        st.write("### Uploaded Image")
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)

        st.write("### Processing Image...")
        b64image_data = encode_image_to_base64(uploaded_file)  # Encode the image
        response = send_to_llama_api(b64image_data)  # Send to LLaMA API

        if response:
            st.write("### LLaMA API Response")
            st.json(response)  # Display API response as JSON
        else:
            st.error("Failed to get a response from the LLaMA API.")

if __name__ == "__main__":
    main()
