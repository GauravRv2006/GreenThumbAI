import os
import streamlit as st
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from datetime import datetime
from PIL import Image
from dotenv import load_dotenv
import base64

# Load environment variables from .env file
load_dotenv()

# Custom CSS for positioning logo and title
st.markdown(
    """
    <style>
    .logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 200px;  /* Adjust width as needed */
        padding-top: 10px; /* Space between logo and title */
    }
    .title {
        text-align: center;
        font-size: 36px;
        margin-top: 10px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the logo
logo_path = "D:\GreenThumb_ai\models\WhatsApp Image 2024-08-25 at 10.22.13_0ae9a014.jpg"  # Path to your logo image
# Encode image to base64
def get_base64_of_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

if os.path.isfile(logo_path):
    logo_base64 = get_base64_of_image(logo_path)
    st.markdown(f'<img class="logo" src="data:image/jpeg;base64,{logo_base64}" alt="GreenThumb Logo">', unsafe_allow_html=True)
else:
    st.error("Logo file not found.")

# Display the title
st.markdown('<div class="title">GREENTHUMB AI</div>', unsafe_allow_html=True)

# Main app content
st.write("Welcome to the Plant Doctor App!")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image = None  # Define image here

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

# Configure the generative AI model
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Define the prompt template with placeholders
prompt = """You are Plant Doctor. 
You are tasked with diagnosing the health of the plant in the image. Remember,Don't bother asking for more information to provide a diagnosis. Even if it isn't that accurate, provide an output. Provide the output in sections with respective titles.
Name and species of the plant
Status of the plant: healthy or unhealthy
Observations
Diagnosis and symptoms
Treatment with the dates scheduled for it
General Care Recommendations: Water Schedule, Sunlight Requirement, Pruning and Fertilisation
All the topics I mentioned above, the title ALONE SHOULD BE BOLDED
Today's date is {date}.
Mention on which dates what has to be done from today like a prescription.
Also Mention when should be the next checkup."""

# Create a PromptTemplate object
prompt_template = PromptTemplate(template=prompt)

# Format the prompt with the current date
formatted_prompt = prompt_template.format(date=current_date)

# Initialize the generative model
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

try:
    if image is not None:
        # Generate content using the formatted prompt and image
        response = model.generate_content([formatted_prompt, image])
        
        # Display the response
        if response.text:
            st.write(response.text)
        else:
            st.write("No content returned from the model.")
    else:
        st.write("Please upload an image to get a diagnosis.")
except Exception as e:
    st.error(f"An error occurred: {e}")
