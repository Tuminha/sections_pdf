"""
This file is where we will write the code to extract the conclusion from the XML root.
First, we import the necessary modules.
Second, we check if the GROBID service is already running, and if it is not, we start it.
Third, we send the PDF to GROBID.
Fourth, we save the XML output.
Fifth, we parse the XML output and define the namespace.
Sixth, we find all 'div' elements in the XML and check if the title contains any of the specified sections.
If it does, we print the title of the section and recursively find all 'p' elements in the 'div'.
Then, we print the paragraph text and the text of any 'ref' elements within the paragraph.
Finally, we add a newline after the paragraph.
"""

# First import the necessary modules
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

def extract_conclusion(xml_root: ET.Element, namespace: dict) -> None:
    """
    This function extracts the conclusion from the XML root.
    """
    for div in xml_root.findall('.//tei:div', namespace):
        # Get the title of the section
        title = div.find('tei:head', namespace).text if div.find('tei:head', namespace) is not None else 'No title'
        title = title.strip().lower()  # Remove leading/trailing whitespace and convert to lower case
        # Check if the title contains any of the specified sections
        if title in ['conclusion', 'conclusions', 'discussion and conclusions', 'discussion and conclusion']:
            print(f'Processing section: {title}')  # Debug print
            # Find all 'p' elements in the 'div'
            for paragraph in div.findall('tei:p', namespace):
                # Get the paragraph text
                paragraph_text = paragraph.text if paragraph.text is not None else ''
                paragraph_text = paragraph_text.strip()  # Remove leading/trailing
                # Print the paragraph text
                print(paragraph_text)
                # Find all 'ref' elements in the 'p'
                for ref in paragraph.findall('tei:ref', namespace):
                    # Get the text of the 'ref' element
                    ref_text = ref.text if ref.text is not None else ''
                    ref_text = ref_text.strip()
                    # Print the text of the 'ref' element
                    print(ref_text)
                # Add a newline after the paragraph
                print()
            # Stop processing the XML
            break

# Extract the conclusion
extract_conclusion(root, ns)
