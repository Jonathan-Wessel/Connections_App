import streamlit as st
import openai
from PIL import Image

openai.api_key = "your_openai_api_key"

def get_solution(prompt):
    """Send a prompt to OpenAI and get the solution."""
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

def extract_text_from_image(image):
    """Extract text from an uploaded image using Tesseract OCR."""
    return pytesseract.image_to_string(image)

# Streamlit App
st.title("New York Connections Solver")
st.write("Upload an image, and we'll analyze it for New York-related connections.")

# File uploader for images
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
if uploaded_file:
    # Open the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Optionally extract text from the image
    with st.spinner("Analyzing image..."):
        extracted_text = extract_text_from_image(image)
        st.write("Extracted Text from Image:", extracted_text)

    # Generate a prompt for OpenAI
    prompt = f"Describe how this text relates to New York City: {extracted_text}"
    solution = get_solution(prompt)
    
    # Display the solution
    st.write("Solution:", solution)