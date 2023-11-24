import os
import subprocess
import time
import xml.etree.ElementTree as ET
import requests

# Path to the GROBID service
GROBID_PATH = '/Users/franciscoteixeirabarbosa/projects/test/sections_pdf/grobid'

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
    '/Users/franciscoteixeirabarbosa/projects/test/sections_pdf/data/Implant stability change and osseointegration speed of immediately loaded photofunctionalized implants.pdf'
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

def extract_introduction(xml_root: ET.Element, namespace: dict) -> str:
    """
    This function extracts the introduction from the XML root.
    """
    # Initialize an empty string to store the introduction
    introduction = ""
    capture_text = False

    # Find all 'div' elements in the XML
    for div in xml_root.findall('.//tei:div', namespace):
        # Get the title of the section
        title = div.find('tei:head', namespace)
        title = title.text.strip().lower() if title is not None else ''

        print(f"Processing div with title: {title}")  # Debugging line

        # Start capturing text after the abstract
        if 'abstract' in title:
            capture_text = True
            print("Found abstract, starting to capture text")  # Debugging line
            continue

        # Start capturing text if we haven't started yet and we encounter a div with head 'p'
        if not capture_text and 'p' in title:
            capture_text = True
            print("Found div with head 'p', starting to capture text")  # Debugging line

        # Stop capturing text before the methods
        if 'materials and methods' in title:
            print("Found materials and methods, stopping to capture text")  # Debugging line
            break

        # Capture the text if we're between the abstract and the methods
        if capture_text:
            print("Capturing text")
            # Find all 'p' elements in the 'div'
            for paragraph in div.findall('tei:p', namespace):
                # Get the paragraph text
                paragraph_text = paragraph.text if paragraph.text is not None else ''
                paragraph_text = paragraph_text.strip()  # Remove leading/trailing whitespace
                # Append the paragraph text
                introduction += paragraph_text + "\n"

    # Return the introduction
    return introduction

# Extract the introduction
introduction_for_ai = extract_introduction(root, ns)

# Export the introduction_for_ai variable
__all__ = ['introduction_for_ai']

print(introduction_for_ai)
