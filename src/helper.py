# Adding utility tools
import fitz # PyMuPDF
import os
from dotenv import load_dotenv
from groq import Groq
from apify_client import ApifyClient

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
apify_client = ApifyClient(os.getenv("APIFY_API_KEY"))

def ask_groq(prompt, max_tokens=500): # This function to get the information like summary, gaps and missings, future roadmap
    """
        Sends a prompt to the groq API and return the response.
    Args:
        prompt (str): The prompt to send to the Groq.
        model (str): The model to use for the request.
        temperature (float): The temperature for the response.
    Returns:
        str: The response from the Groq API.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5,
        max_completion_tokens=max_tokens 
    )

    return response.choices[0].message.content
    

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a PDF file.

    Args:
        uploaded_file (str): The path to the PDF file

    Returns:
        str: The extracted text.
    """
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text
        

