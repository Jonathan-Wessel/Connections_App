import streamlit as st
from openai import OpenAI
from PIL import Image
from dotenv import load_dotenv
import pytesseract
import os

load_dotenv()

client = OpenAI(
    api_key = st.secrets["OPEN_API_KEY"],
)

def extract_text_from_image(image):
    """Extract text from an uploaded image using Tesseract OCR."""
    return pytesseract.image_to_string(image)

def get_solution(prompt):
    """Send a prompt to OpenAI and get the solution."""
    answer = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are solving NYT connections"},
            {
                "role": "user",
                "content": "You are going to be solving New York Times connections, these are the words you will be connecting. I just want the final answers in your response, nothing esle. Give me your finalized answers in a bulleted list seperated by commas of the four groups, "+prompt+""
            }
        ]
    )
    return answer.choices[0].message.content

# Streamlit App
st.title("NYT Connections Solver")
st.write("Upload an image, and we'll give you the correct solution.")



# File uploader for images
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
if uploaded_file:
    # Open the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Optionally extract text from the image
    with st.spinner("Analyzing image..."):
        extracted_text = extract_text_from_image(image)
        st.write("Extracted Text from Image:", extracted_text)

    # Generate a prompt for OpenAI
    prompt = f"These are NYT connections words: {extracted_text}"
    solution = get_solution(prompt)
    
    # Display the solution
    st.write("Solution:", solution)