import streamlit as st
from openai import OpenAI
from PIL import Image
import pytesseract


client = OpenAI()

client.api_key = "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"


def get_solution(prompt):
    """Send a prompt to OpenAI and get the solution."""
    answer = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are solving NYT connections"},
            {
                "role": "user",
                "content": ""+prompt+""
            }
        ]
    )
    return answer.choices[0].message

def extract_text_from_image(image):
    """Extract text from an uploaded image using Tesseract OCR."""
    return pytesseract.image_to_string(image)

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
    prompt = f"Describe how this text relates to New York City: {extracted_text}"
    solution = get_solution(prompt)
    
    # Display the solution
    st.write("Solution:", solution)