"""
In this part of the code, an AI agent will use the function to extract the introduction from a pdf file.
The function to extract the introduction is in the introduction.py file, so we need to import it.
After it, the AI agent will analyze the introduction based on a customized prompt.
"""

# 1. Import the necessary libraries and functions
from introduction import introduction_for_ai

from openai import OpenAI
from dotenv import load_dotenv
import os

# Load OpenAI API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set OpenAI API key
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize variables
system_message = {
    "role": "system", 
    "content": "You are a critical-thinking AI trained to analyze scientific articles meticulously. \
Your role is to critically evaluate each section of the article, looking for gaps, flaws, and inconsistencies."
    }
user_message = {
    "role": "user",
    "content": f"""Critically evaluate the introduction of this scientific article: {introduction_for_ai}
    - Does it establish the context of the research? 
    - Are prior studies appropriately cited? 
    - Is there a clear research question or hypothesis?"""
    }

# Use the AI agent to analyze the introduction
print(user_message['content']) 
response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[system_message, user_message],
    max_tokens=3000,
    temperature=0.4
    )

# Print the AI's analysis
print(response.choices[0].message.content)
# Prepare the output to be passed to app.py as introduction_analysis_for_ai
introduction_analysis_for_ai = response.choices[0].message.content
