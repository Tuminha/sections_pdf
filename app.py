# The purpose of APP is to consolidate the results from 1_abstract_analysis.py, 2_introduction_analysis.py, 3_methods_analysis.py, 4_results_analysis.py, 5_discussion_analysis.py and 6_conclusion_analysis.py.
# An AI agent will be used to collectively analyze all the inputs from its AI counterparts.
# This implies that we need to call the functions from the main files, obtain the analysis for each section, and analyze all the sections collectively.
# A detailed prompt should be provided to the AI agent, instructing it to take a step-by-step approach to analyze each section, and link them together to fill in the gaps.
# The AI agent should be on the lookout for inconsistencies, gaps in the article's logic, bias, and red flags.
# The AI agent should also be comparing the article to best practices in scientific research.
# In the next phase, we will use the Perplexity API to compare the article with recent publications and the cited bibliography.

import os
from dotenv import load_dotenv
import openai
from abstract import extract_abstract
from introduction import extract_introduction
from methods import methods_for_ai
from results import results_for_ai
from discussion import discussion_for_ai
from conclusion import conclusion_for_ai

# Load OpenAI API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

def analyze_pdf(pdf_path):
    # Extract each section of the PDF
    abstract = extract_abstract(pdf_path)
    introduction = extract_introduction(pdf_path)
    methods = methods_for_ai(pdf_path)
    results = results_for_ai(pdf_path)
    discussion = discussion_for_ai(pdf_path)
    conclusion = conclusion_for_ai(pdf_path)

    # Analyze each section
    analyze_abstract(abstract)
    analyze_introduction(introduction)
    analyze_methods(methods)
    analyze_results(results)
    analyze_discussion(discussion)
    analyze_conclusion(conclusion)

def analyze_abstract(abstract):
    # Call the function from 1_abstract_analysis.py
    pass

def analyze_introduction(introduction):
    # Call the function from 2_introduction_analysis.py
    pass

def analyze_methods(methods):
    # Call the function from 3_methods_analysis.py
    pass

def analyze_results(results):
    # Call the function from 4_results_analysis.py
    pass

def analyze_discussion(discussion):
    # Call the function from 5_discussion_analysis.py
    pass

def analyze_conclusion(conclusion):
    # Call the function from 6_conclusion_analysis.py
    pass

if __name__ == "__main__":
    pdf_path = '/Users/franciscoteixeirabarbosa/projects/test/sections_pdf/data/Implant survival rates after osteotome_mediated maxillary sinus augmentation_ a systematic review.pdf'
    analyze_pdf(pdf_path)