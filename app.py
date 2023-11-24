from dotenv import load_dotenv
from openai import OpenAI
import os

from abstract_analysis import abstract_analysis_for_ai
from introduction_analysis import introduction_analysis_for_ai
from methods_analysis import methods_analysis_for_ai
from results_analysis import results_analysis_for_ai
from discussion_analysis import discussion_analysis_for_ai
from conclusion_analysis import conclusion_analysis_for_ai

# Load OpenAI API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set OpenAI API key
client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_pdf(pdf_path):
    abstract = abstract_analysis_for_ai
    introduction = introduction_analysis_for_ai
    methods = methods_analysis_for_ai
    results = results_analysis_for_ai
    discussion = discussion_analysis_for_ai
    conclusion = conclusion_analysis_for_ai
    combined_analysis(abstract, introduction, methods, results, discussion, conclusion)

def combined_analysis(abstract, introduction, methods, results, discussion, conclusion):
    system_message = {
        "role": "system",
        "content": "You are a helpful assistant that analyzes scientific articles."
    }
    user_message = {
        "role": "user",
        "content": f"""Critically evaluate the results of the analysis of the different sections of the scientific article,
        your AI colleagues already did the hard work of analyzing the different sections of the article, now it's your turn to analyze the article as a whole.
        With the output from the different sections, you should be able to analyze the article as a whole.
        - Are there any signs of bias?
        - Are there any red flags?
        - Are there any inconsistencies?
        - Are there any gaps in the article's logic?
        - Are there any considerations regarding the best practices in scientific research?
        Here are the outputs from the different sections of the article:
        Abstract: {abstract}
        Introduction: {introduction}
        Methods: {methods}
        Results: {results}
        Discussion: {discussion}
        Conclusion: {conclusion}
        """
    }

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[system_message, user_message],
        max_tokens=4096,
        temperature=0.4
    )
    print("The final analysis is: " + response.choices[0].message.content)

if __name__ == "__main__":
    pdf_path = '/Users/franciscoteixeirabarbosa/projects/test/sections_pdf/data/Implant survival rates after osteotome_mediated maxillary sinus augmentation_ a systematic review.pdf'
    print("Debug: Starting analysis of PDF at path: ", pdf_path)
    analyze_pdf(pdf_path)
