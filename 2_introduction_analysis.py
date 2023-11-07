"""
In this part of the code, an AI agent will use the function to extract the introduction from a pdf file.
The function to extract the introduction is in the introduction.py file, so we need to import it.
After it, the AI agent will analyze the introduction based on a customized prompt.
"""

# 1. Import the necessary libraries and functions
import xml.etree.ElementTree as ET
from introduction import extract_introduction

import openai
import requests
from dotenv import load_dotenv
import os




# Path to the PDF file
PDF_PATH = 'data/Implant_abutment interface_ biomechanical study of flat top versus conical.pdf'

print("Current working directory:", os.getcwd())
print("File exists:", os.path.exists(PDF_PATH))

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


# Extract the introduction
introduction = extract_introduction(PDF_PATH, ns)
print(f"Introduction: {introduction}")

prompt_introduction = f"Introduction: Perform a detailed analysis of the {introduction}. \
    - Does it establish the context of the research? \
    - Are prior studies appropriately cited? \
    - Is there a clear research question or hypothesis?"

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
    "content": prompt_introduction
    }

# Use the AI agent to analyze the introduction
print(prompt_introduction) 
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[system_message, user_message],
    max_tokens=3000  # Increased token limit
)

# Print the AI's analysis
print(response.choices[0].message['content'])