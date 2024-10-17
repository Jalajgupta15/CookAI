import streamlit as st
from clarifai.client.model import Model
from PIL import Image
import requests
from io import BytesIO
from googleapiclient.discovery import build


# API Keys
clarifai_pat = "5a2c5e444b9b40ab9e4f60f950e71bfd"  # Your Clarifai PAT
themealdb_api_key = "1"  # Test API Key for TheMealDB
google_api_key = 'AIzaSyAdj0qB_7Z5LuTosBkI_oY47USIZ_MtvVU'  # Your YouTube API Key


# YouTube Search Function
def get_youtube_video(dish_name):
    youtube = build('youtube', 'v3', developerKey=google_api_key)
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=f"{dish_name} recipe"
    )
    response = request.execute()
    video_id = response['items'][0]['id']['videoId']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    return video_url


# Clarifai API Function to Recognize Dish from Image (Using Bytes)
def recognize_dish(image_bytes):
    model_url = "https://clarifai.com/clarifai/main/models/food-item-recognition"
    model = Model(url=model_url, pat=clarifai_pat)
   
    # Call Clarifai's predict method
    model_prediction = model.predict_by_bytes(image_bytes, input_type="image")
   
    if model_prediction and model_prediction.outputs:
        return model_prediction.outputs[0].data.concepts[0].name  # Access name correctly
    else:
        st.error("Error in fetching data from Clarifai API.")
        return None


# TheMealDB API Function to Get Recipe Details
def get_recipe_data(dish_name):
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={dish_name}"
    response = requests.get(url)
    if response.status_code == 200 and response.json()['meals']:
        return response.json()['meals'][0]
    else:
        st.error(f"No recipe found for {dish_name}.")
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
    try:
        # Convert to bytes using PIL
        image_bytes = BytesIO()
        image.save(image_bytes, format='PNG')  # Save the image in bytes
        image_bytes.seek(0)  # Move to the start of the BytesIO object
       
        # Call the Clarifai API to recognize the dish
        st.write("Analyzing the dish... ⏳")
       
        dish_name = recognize_dish(image_bytes.read())  # Read bytes for prediction
       
        if dish_name:
            st.write(f"### Dish Name: {dish_name}")
           
            # Get recipe details from TheMealDB
            recipe_data = get_recipe_data(dish_name)
           
            if recipe_data:
                # Display ingredients
                st.write("### Ingredients:")
                for i in range(1, 21):  # 1 to 20
                    ingredient = recipe_data.get(f'strIngredient{i}')
                    measure = recipe_data.get(f'strMeasure{i}')
                    if ingredient:
                        st.write(f"- {ingredient} ({measure})")


                # Provide recipe instructions
                st.write("### Recipe:")
                st.write(recipe_data['strInstructions'])
               
                # Fetch and display a relevant YouTube video
                st.write("### Watch a relevant recipe video:")
                video_url = get_youtube_video(dish_name)
                st.video(video_url)
            else:
                st.write(f"No recipe data found for {dish_name}.")
        else:
            st.write("Unable to recognize the dish. Please try another image.")
    except Exception as e:
        st.error(f"An error occurred while processing the image: {e}")


# Footer credits
st.markdown("---")
st.markdown("#### Created by Jalaj and Ishan 👨‍🍳")



