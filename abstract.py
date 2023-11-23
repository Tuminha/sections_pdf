"""
This module is used for parsing XML files, managing subprocesses, and handling time-related functions.
"""

import re
import xml.etree.ElementTree as ET
import subprocess
import time
import requests

# Path to the GROBID service
GROBID_PATH = '/Users/franciscoteixeirabarbosa/projects/test/sections_pdf/grobid'

# First check if the GROBID service is already running, and if it already running do not start it again
# Check if the GROBID service is already running
try:
    response = requests.get('http://localhost:8070/api/isalive', timeout=10)
    if response.status_code == 200:
        print("GROBID service is already running.")
    else:
        # Start the GROBID service
        p = subprocess.Popen(['./gradlew', 'run', '--stacktrace'], cwd=GROBID_PATH)
        # Wait for the GROBID service to start
        time.sleep(10)
except requests.exceptions.RequestException as e:
    # If the request fails, it means the service is not running
    print("GROBID service is not running. Starting it now...")
    p = subprocess.Popen(['./gradlew', 'run', '--stacktrace'], cwd=GROBID_PATH)
    # Wait for the GROBID service to start
    time.sleep(10)

# Wait for the GROBID service to start
time.sleep(10)

PDF_PATH = (
    '/Users/franciscoteixeirabarbosa/projects/test/sections_pdf/data/Implant survival rates after osteotome_mediated maxillary sinus augmentation_ a systematic review.pdf'
)

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

def abstract_for_ai(xml_root: ET.Element, namespace: dict) -> str:
    """
    This function extracts the abstract from the XML root.

    Parameters:
    xml_root (ET.Element): The root of the XML document.
    namespace (dict): The namespace for the XML document.

    Returns:
    str: The abstract text.
    """
    abstract = xml_root.find('.//tei:abstract', namespace)
    if abstract is not None:
        return "".join(abstract.itertext())
    return ""

# Call the function
abstract_for_ai = abstract_for_ai(root, ns)
# New line
print(abstract_for_ai)
