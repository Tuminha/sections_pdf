'''
In this file, we aim to after extracting the different sections with the functions present in abstract.py, 
introduction.py, methods.py, results.py, discussion.py, conclusion.py and bibliography.py, 
we want to create a json file with the following structure:
Title:
Authors:
Year of Publication:
Abstract:
Introduction:
Methods:
Results:
Discussion:
Conclusion:
Bibliography:

The steps to achieve this goal are:
1. Import the necessary libraries and functions
2. Define the functions to extract the different sections
3. Define the function to create the json file
4. Use the functions from the other files to extract the different sections
5. Create the json file

'''

# 1. Import the necessary libraries and functions
import json
import xml.etree.ElementTree as ET
from abstract import extract_title, extract_authors, extract_year, extract_abstract
from introduction import extract_introduction
from methods import extract_methods
from results import extract_results
