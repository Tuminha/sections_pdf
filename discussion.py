"""
This files is where the discussion section is extracted from the XML root.
First, we check if GROBID is running. If it is not, we start it. Then, we send the PDF to GROBID and save the XML output.
Next, we parse the XML output and define the namespace. Then, we find all 'div' elements in the XML and check if the title contains any of the specified sections.
If it does, we print the title of the section and recursively find all 'p' elements in the 'div'. Then, we print the paragraph text and the text of any 'ref' elements within the paragraph.
Finally, we add a newline after the paragraph.
"""

import subprocess
import time
import xml.etree.ElementTree as ET
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
        grobid_process = subprocess.Popen(['./gradlew', 'run', '--stacktrace'], cwd=GROBID_PATH)
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

def extract_discussion(xml_root: ET.Element, namespace: dict) -> str:
    """
    This function extracts the discussion from the XML root.
    """
    # Initialize an empty string to store the discussion
    discussion = ""

    # Find all 'div' elements in the XML
    for div in xml_root.findall('.//tei:div', namespace):
        # Get the title of the section
        title = div.find('tei:head', namespace).text if div.find('tei:head', namespace) is not None else 'No title'
        title = title.strip().lower()  # Remove leading/trailing whitespace and convert to lower case
        # Check if the title contains any of the specified sections
        if title in ['discussion', 'discussion and conclusion', 'discussion and conclusions', 'discussion and future work', 'discussion and future directions', 'discussion and future perspectives', 'discussion and future research', 'discussion and implications', 'discussion and limitations', 'discussion and outlook', 'discussion and practical implications', 'discussion and recommendations', 'discussion and summary', 'discussion and conclusions', 'discussion/conclusion', 'discussion/conclusions', 'discussion/conclusions and future work', 'discussion/conclusions and future directions', 'discussion/conclusions and future perspectives', 'discussion/conclusions and future research', 'discussion/conclusions and implications', 'discussion/conclusions and limitations', 'discussion/conclusions and outlook', 'discussion/conclusions and practical implications', 'discussion/conclusions and recommendations', 'discussion/conclusions and summary', 'discussion/conclusions and summary and future work', 'discussion/conclusions/implications', 'discussion/conclusions/recommendations', 'discussion/summary', 'discussion/summary and conclusion', 'discussion/summary and conclusions', 'discussion/summary and future work', 'discussion/summary and future directions', 'discussion/summary and future perspectives', 'discussion/summary and future research', 'discussion/summary and implications', 'discussion/summary and limitations', 'discussion/summary and outlook', 'discussion/summary and practical implications', 'discussion/summary and recommendations', 'discussion/summary and summary', 'discussion/summary/conclusion', 'discussion/summary/conclusions', 'discussion/summary/recommendations']:
            discussion += f'Processing section: {title}\n'  # Debug print
            # Find all 'p' elements in the 'div'
            for paragraph in div.findall('tei:p', namespace):
                # Get the paragraph text
                paragraph_text = paragraph.text if paragraph.text is not None else ''
                paragraph_text = paragraph_text.strip()  # Remove leading/trailing
                # Append the paragraph text
                discussion += paragraph_text + "\n"
                # Find all 'ref' elements in the 'p'
                for ref in paragraph.findall('tei:ref', namespace):
                    # Get the text of the 'ref' element
                    ref_text = ref.text if ref.text is not None else ''
                    ref_text = ref_text.strip()
                    # Append the text of the 'ref' element
                    discussion += ref_text + "\n"
            # Stop processing the XML
            break

    # Return the discussion
    return discussion

# Extract the discussion
discussion_for_ai = extract_discussion(root, ns)

# Export the discussion_for_ai variable
__all__ = ['discussion_for_ai']

#New line

#

