# Here we will create a function extract_introduction to extract the introduction from the XML root.

# First import the necessary modules
import xml.etree.ElementTree as ET
import re
import requests
import subprocess
import time

# Path to the GROBID service
grobid_path = '/Users/franciscoteixeirabarbosa/projects/test/sections_pdf/grobid'


# First check if the GROBID service is already running, and if it already running do not start it again
# Check if the GROBID service is already running
try:
    response = requests.get('http://localhost:8070/api/isalive', timeout=10)
    if response.status_code == 200:
        print("GROBID service is already running.")
    else:
        # Start the GROBID service
        p = subprocess.Popen(['./gradlew', 'run', '--stacktrace'], cwd=grobid_path)
        # Wait for the GROBID service to start
        time.sleep(10)
except requests.exceptions.RequestException as e:
    # If the request fails, it means the service is not running
    print("GROBID service is not running. Starting it now...")
    p = subprocess.Popen(['./gradlew', 'run', '--stacktrace'], cwd=grobid_path)
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

# Define the extract_introduction function
def extract_introduction(xml_root: ET.Element, namespace: dict) -> None:
    """
    This function extracts the introduction from the XML root.

    Parameters:
    xml_root (ET.Element): The root of the XML document.
    namespace (dict): The namespace for the XML document.

    Returns:
    None
    """
    # Mapping dictionary to associate various section names with generalized names
    section_mappings = {
        'Introduction': ['introduction', 'summary', 'background', 'background and aims', 'background and purpose', 'background and objective', 'background and objectives', 'background and rationale', 'background and significance', 'background information', 'context', 'context and background', 'context and objective', 'context and objectives', 'context and rationale', 'context and significance', 'context and study design', 'context and study objective', 'context and study objectives', 'context and study rationale', 'context and study significance', 'context a'],
    }

    # Find all 'div' elements in the XML
    for div in xml_root.findall('.//tei:div', namespace):
        # Get the title of the section
        title = div.find('tei:head', namespace)
        if title is not None:
            title = title.text.strip().lower()  # Remove leading/trailing whitespace and convert to lower case

            # Check if the title contains any of the specified sections
            for section, variants in section_mappings.items():
                if any(variant in title for variant in variants):
                    print(f'\n{section}:\n')
                    
                    # Get the paragraphs of the section
                    paragraphs = [''.join(p.itertext()) for p in div.findall('.//tei:p', namespace)]
                    full_text = ' '.join(paragraphs)
                    print(full_text)

# Call the function
extract_introduction(root, ns)
