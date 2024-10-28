# Import necessary libraries
import os
import json
import tempfile
from PIL import Image
import io
import base64
import streamlit as st
import requests



genai.configure(api_key='xxx')
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

    myfile = genai.upload_file(temp_file_path)
    model = genai.GenerativeModel("gemini-1.5-flash")

    result = model.generate_content(
        [myfile, "\\n\\n", "Please extract all eatable product names from this receipt."],
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=list[str]
        ),
    )
    return result.text

def clean_product_names(product_list):
    model = genai.GenerativeModel("gemini-1.5-flash")
    result_clean = model.generate_content(
        [f"Please suggest clean, simple names for product names from this list: {product_list}"],
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=list[str]
        ),
    )
    return result_clean.text

# def get_calories_from_usda(food_name, api_key=USDA_API_KEY):
#     url = "https://api.nal.usda.gov/fdc/v1/foods/search"
#     params = {
#         "query": food_name,
#         "pageSize": 1,
#         "api_key": api_key
#     }
#     response = requests.get(url, params=params)
#     data = response.json()

#     if "foods" in data and data["foods"]:
#         food_data = data["foods"][0]
#         description = food_data.get("description", "Unknown item")
#         calories = food_data.get("foodNutrients", [{}])[0].get("value", "Calories not found")
#         return description, calories
#     else:
#         return "Item not found", "Calories not found"

def run_calorie_tracker_app():
    st.title("AIU - Calorie Tracker")
    st.write("Upload or capture a receipt image to analyze it.")

    uploaded_file = st.file_uploader("Upload or capture a receipt image", type=["jpg", "jpeg", "png", "webp", "heic", "heif"])

    if uploaded_file is not None:
        st.write("### Step 1: Extracting Product Names")
        raw_product_names = extract_product_names(uploaded_file)
        st.write("Extracted Product Names:", raw_product_names)

        st.write("### Step 2: Cleaning Product Names")
        cleaned_product_names = clean_product_names(raw_product_names)
        st.write("Cleaned Product Names:", cleaned_product_names)  # Display cleaned product names

        # Convert cleaned product names to a Python list
        products = json.loads(cleaned_product_names)

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
