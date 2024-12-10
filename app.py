import streamlit as st
from openai import OpenAI
from PIL import Image
from dotenv import load_dotenv
import pytesseract
import os

st.set_page_config(page_title="NYT Connections Solver", page_icon="🧩", layout="wide")

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=st.secrets["OPEN_API_KEY"],
)

# Custom CSS for styling
st.markdown(
    """
    <style>
        /* Global styles */
        body {
            background-color: #f0f2f6;
            font-family: 'Arial', sans-serif;
        }
        .main {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stSidebar {
            background-color: #4CAF50;
            color: white;
        }
        h1 {
            color: #4CAF50;
        }
        h2, h3 {
            color: #333333;
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            border-radius: 5px;
            padding: 10px 20px;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Functions
def extract_text_from_image(image):
    """Extract text from an uploaded image using Tesseract OCR."""
    return pytesseract.image_to_string(image)

def get_solution(prompt):
    """Send a prompt to OpenAI and get the solution."""
    answer = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are solving NYT connections."},
            {
                "role": "user",
                "content": (
                    "You are going to be solving New York Times connections. "
                    "These are the words you will be connecting. I just want the final answers in your response, "
                    "nothing else. Give me your finalized answers in a bulleted list separated by commas of the four groups, I also want you to add line breaks like in a strang to make a new line for each group: "
                    + prompt
                ),
            },
        ],
    )
    return answer.choices[0].message.content

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Upload Image", "Solved Connections"])

if page == "Upload Image":
    st.title("🖼️ Upload NYT Connections Image")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Extract text from the image
        with st.spinner("Extracting text..."):
            extracted_text = extract_text_from_image(image)
            st.session_state["extracted_text"] = extracted_text  # Store text in session state
            st.success("Text extracted successfully! Navigate to 'Solved Connections' to see the solution.")

elif page == "Solved Connections":
    st.title("✅ Solved Connections")

    # Check if text was extracted
    if "extracted_text" in st.session_state:
        extracted_text = st.session_state["extracted_text"]

        # Generate solution
        with st.spinner("Generating solution..."):
            prompt = f"These are NYT connections words: {extracted_text}"
            solution = get_solution(prompt)
            

        # Display the solution
        st.markdown(
            f"""
            <div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px;">
                <h3>Solution</h3>
                <p>{solution}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error("No text found. Please go back to 'Upload Image' to upload an image.")
