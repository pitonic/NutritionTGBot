# Import necessary libraries
import os
import json
import tempfile
from PIL import Image
import io
import base64
import streamlit as st
import requests

# Define the URL for the local LLaMA 3.2 API
LLAMA_API_URL = "http://tower.nicolai.top:11434/api/generate"

# USDA API Key
USDA_API_KEY = "xxx"

def extract_product_names(file):
    # Map MIME types to file extensions
    mime_to_extension = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "image/heic": ".heic",
        "image/heif": ".heif"
    }
    file_extension = mime_to_extension.get(file.type)

    if not file_extension:
        st.error("Unsupported file type.")
        return None

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        temp_file.write(file.getbuffer())
        temp_file_path = temp_file.name

    # Prepare the payload for the LLaMA API
    with open(temp_file_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    payload = {
        "model": "llava-llama3",
        "prompt": "Please extract all eatable product names from this receipt.",
        "stream": False,
        "images": [image_data]
    }

    try:
        # Send the request to the LLaMA API
        response = requests.post(LLAMA_API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()

        if "product_names" in result:
            return result["product_names"]
        else:
            st.error("Failed to extract product names. Unexpected response format.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to LLaMA API: {e}")
        return None

def clean_product_names(product_list):
    # Prepare the payload for the LLaMA API
    payload = {
        "model": "llava-llama3",
        "prompt": f"Please suggest clean, simple names for product names from this list: {product_list}",
        "stream": False
    }

    try:
        # Send the request to the LLaMA API
        response = requests.post(LLAMA_API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()

        if "cleaned_names" in result:
            return result["cleaned_names"]
        else:
            st.error("Failed to clean product names. Unexpected response format.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to LLaMA API: {e}")
        return None

def get_calories_from_usda(food_name, api_key=USDA_API_KEY):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "query": food_name,
        "pageSize": 1,
        "api_key": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "foods" in data and data["foods"]:
        food_data = data["foods"][0]
        description = food_data.get("description", "Unknown item")
        calories = food_data.get("foodNutrients", [{}])[0].get("value", "Calories not found")
        return description, calories
    else:
        return "Item not found", "Calories not found"

def run_calorie_tracker_app():
    st.title("AIU - Calorie Tracker")
    st.write("Upload or capture a receipt image to analyze it.")

    uploaded_file = st.file_uploader("Upload or capture a receipt image", type=["jpg", "jpeg", "png", "webp", "heic", "heif"])

    if uploaded_file is not None:
        st.write("### Step 1: Extracting Product Names")
        raw_product_names = extract_product_names(uploaded_file)
        if raw_product_names:
            st.write("Extracted Product Names:", raw_product_names)

            st.write("### Step 2: Cleaning Product Names")
            cleaned_product_names = clean_product_names(raw_product_names)
            if cleaned_product_names:
                st.write("Cleaned Product Names:", cleaned_product_names)  # Display cleaned product names

                try:
                    # Convert cleaned product names to a Python list
                    products = json.loads(cleaned_product_names)
                except json.JSONDecodeError:
                    st.error("Failed to parse cleaned product names. Invalid JSON format.")
                    return

                st.write("### Step 3: Calorie Information")
                product_data = []
                total_calories = 0

                for product in products:
                    description, calories = get_calories_from_usda(product, USDA_API_KEY)
                    if isinstance(calories, (int, float)):
                        total_calories += calories
                    product_data.append({
                        "Product": product,
                        "Description": description,
                        "Calories per 100g": calories
                    })

                st.table(product_data)
                st.write(f"### Total Calories: {total_calories} per 100g")

if __name__ == "__main__":
    run_calorie_tracker_app()
