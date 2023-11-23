"""
In this part of the code, an AI agent will use the function to extract the methods from a pdf file.
The function to extract the methods is in the methods.py file, so we need to import it.
After it, the AI agent will analyze the methods based on a customized prompt.
"""


# 1. Import the necessary libraries and functions
import xml.etree.ElementTree as ET
from methods import methods_for_ai

import openai
import requests
from dotenv import load_dotenv
import os

# Path to the PDF file
PDF_PATH = ('/Users/franciscoteixeirabarbosa/projects/test/sections_pdf/data/Implant survival rates after osteotome_mediated maxillary sinus augmentation_ a systematic review.pdf')


# Send the PDF to GROBID
with open(PDF_PATH, 'rb') as f:
    response = requests.post('http://localhost:8070/api/processFulltextDocument', files={'input': f}, timeout=10)

# Save the XML output
with open('output.xml', 'w', encoding='utf-8') as f:
    f.write(response.text)

# Parse the XML output
tree = ET.parse('output.xml')
root = tree.getroot()

# Define the namespace
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

# Parse the XML file
tree = ET.parse('output.xml')
root = tree.getroot()


# Extract the methods
print(f"Methods: {methods_for_ai}")

prompt_methods = f"""Critically evaluate the methods of this scientific article: {methods_for_ai}
    - Are the methods clearly presented?
    - Are there any signs of bias in the methods?
    - Are the conclusions supported by the methods?
    - Are there any red flags or parts we should take a close look at?
    - Are there any considerations regarding material and methods and best practices in scientific investigation?
    """

# Load OpenAI API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY


# Check if the API key is valid and working

response = openai.Completion.create(
    engine="davinci",
    prompt="This is a test",
    max_tokens=5
)

print(response)

# Initialize variables
system_message = {
    "role": "system", 
    "content": "You are a critical-thinking AI trained to analyze scientific articles meticulously. \
Your role is to critically evaluate each section of the article, looking for gaps, flaws, and inconsistencies."
    }
user_message = {
    "role": "user",
    "content": prompt_methods
    }

# Use the AI agent to analyze the methods
print(prompt_methods) 
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[system_message, user_message],
    max_tokens=3000  # Increased token limit
)

# Print the AI's analysis
print(response.choices[0].message['content'])