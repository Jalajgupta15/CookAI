mport streamlit as st
from clarifai.client import ClarifaiApp
from PIL import Image
import requests
from io import BytesIO

# API Keys
clarifai_pat = "5a2c5e444b9b40ab9e4f60f950e71bfd"  # Your Clarifai PAT
edamam_app_id = "c5489fa8"  # Your Edamam Application ID
edamam_app_key = "28c649aea6659a58e66f20282bcba885"  # Your Edamam Application Key
google_api_key = 'AIzaSyAdj0qB_7Z5LuTosBkI_oY47USIZ_MtvVU'  # Your YouTube API Key

# Initialize Clarifai App
clarifai_app = ClarifaiApp(api_key=clarifai_pat)

# YouTube Search Function
def get_youtube_video(dish_name):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={dish_name}+recipe&type=video&key={google_api_key}"
    response = requests.get(url).json()
    if response.get('items'):
        video_id = response['items'][0]['id']['videoId']
        return f"https://www.youtube.com/watch?v={video_id}"
    return None

# Clarifai API Function to Recognize Dish from Image
def recognize_dish(image_bytes):
    model = clarifai_app.models.get('food-item-recognition')
    response = model.predict_by_bytes(image_bytes)
    
    if response['outputs']:
        return response['outputs'][0]['data']['concepts'][0]['name']  # Get dish name
    else:
        st.error("Error in fetching data from Clarifai API.")
        return None

# Edamam API Function to Get Nutritional Information
def get_nutrition_data(dish_name):
    url = f"https://api.edamam.com/api/nutrition-details"
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "ingredients": [
            {
                "text": dish_name
            }
        ]
    }
    params = {
        "app_id": edamam_app_id,
        "app_key": edamam_app_key
    }
    response = requests.post(url, headers=headers, json=payload, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return {
            'calories': round(data['calories']),
            'serving_size': data['yield']  # Number of servings
        }
    else:
        st.error(f"No nutritional data found for {dish_name}.")
        return None

# Streamlit App Interface
st.title('CookAI 🍳')
st.write("## Upload an image of your dish to get its name, ingredients, calories, recipe, and a YouTube tutorial!")
st.write("### Supports Continental dishes")

# File uploader
uploaded_file = st.file_uploader("Upload an image of the dish (jpeg, png, jpg):", type=["jpeg", "png", "jpg"])

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Convert image to bytes for prediction
    image_bytes = BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)

    # Recognize the dish using Clarifai
    st.write("Analyzing the dish... ⏳")
    dish_name = recognize_dish(image_bytes.read())

    if dish_name:
        st.write(f"### Dish Name: {dish_name}")

        # Get nutritional details from Edamam
        nutrition_data = get_nutrition_data(dish_name)
        
        if nutrition_data:
            # Display calories and serving size
            st.write("### Nutritional Information:")
            st.write(f"- Calories: {nutrition_data['calories']} kcal")
            st.write(f"- Serving Size: {nutrition_data['serving_size']} servings")

            # Fetch and display a relevant YouTube video
            st.write("### Watch a relevant recipe video:")
            video_url = get_youtube_video(dish_name)
            if video_url:
                st.video(video_url)
            else:
                st.write("No video found.")
        else:
            st.write("No nutritional data found.")
    else:
        st.write("Unable to recognize the dish. Please try another image.")

# Footer credits
st.markdown("---")
st.markdown("#### Created by Jalaj and Ishan 👨‍🍳")
