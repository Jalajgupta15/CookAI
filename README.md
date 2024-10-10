
# CookAI 🍳

**CookAI** is a user-friendly web application that allows you to upload an image of a dish and receive its name, ingredients, calories, and a relevant recipe tutorial from YouTube. Built using Streamlit, Clarifai for image recognition, and TheMealDB for recipe information, CookAI supports a wide range of continental dishes.

## Features
- **Image Recognition**: Automatically identifies the dish from the uploaded image using Clarifai's food-item recognition model.
- **Recipe Retrieval**: Fetches detailed recipe information, including ingredients and instructions, from TheMealDB.
- **YouTube Integration**: Provides a link to a YouTube video tutorial for the identified dish.
- **User-Friendly Interface**: Simple and intuitive design for easy navigation and interaction.

## Demo Video
[Click here to watch the demo video](https://drive.google.com/file/d/1BTieIYTUzErnKk0H0uFPskcm4Qm_s4zf/view?usp=sharing)

## How It Works
1. **Upload an Image**: Users upload an image of their dish (jpeg, png, jpg).
2. **Dish Recognition**: The application uses Clarifai's API to recognize the dish from the image.
3. **Recipe Retrieval**: If the dish is recognized, the application fetches the recipe details from TheMealDB.
4. **Video Tutorial**: A YouTube video related to the dish is displayed for visual guidance.

## Technologies Used
- **Streamlit**: For creating the web application interface.
- **Clarifai API**: For recognizing dishes from images.
- **TheMealDB API**: For retrieving recipe details.
- **Google YouTube API**: For fetching related YouTube videos.

## API Keys
- **Clarifai API Key**: Replace the placeholder with your Clarifai personal access token.
- **TheMealDB API Key**: This project uses a test API key.
- **Google YouTube API Key**: Replace the placeholder with your Google YouTube API key.

## Setup & Installation
To run this application locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/CookAI.git
   ```
2. Navigate to the project directory:
   ```bash
   cd CookAI
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your API keys in the code by replacing the placeholders with your actual keys.
5. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage
1. Access the application by visiting the local URL provided by Streamlit after running the app.
2. Upload an image of a dish to see its name, ingredients, recipe instructions, and a YouTube tutorial.

## License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.

## Credits
 Jalaj 👨‍🍳
