import xml.etree.ElementTree as ET
import subprocess
import time
import xml.etree.ElementTree as ET
from typing import Any
import requests
import re

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

def extract_title(xml_root: ET.Element, namespace: dict) -> None:
    """
    This function extracts the title from the XML root.

    Parameters:
    xml_root (ET.Element): The root of the XML document.
    namespace (dict): The namespace for the XML document.

    Returns:
    None
    """
    title = xml_root.find('.//tei:title', namespace)
    if title is not None:
        print(f'Title: {title.text}')

def extract_authors(xml_root: ET.Element, namespace: dict) -> None:
    """
    This function extracts the authors from the XML root.

    Parameters:
    xml_root (ET.Element): The root of the XML document.
    namespace (dict): The namespace for the XML document.

    Returns:
    None
    """
    authors = xml_root.findall('.//tei:sourceDesc/tei:biblStruct/tei:analytic/tei:author/tei:persName', namespace)
    for author in authors:
        forenames = [forename.text for forename in author.findall('tei:forename', namespace)]
        surname = author.find('tei:surname', namespace)
        if surname is not None:
            print('Author: ' + ' '.join(forenames + [surname.text]))


def extract_year(xml_root: ET.Element, namespace: dict) -> None:
    """
    This function extracts the year of publication from the XML root.

    Parameters:
    xml_root (ET.Element): The root of the XML document.
    namespace (dict): The namespace for the XML document.

    Returns:
    None
    """
    date_element = xml_root.find('.//tei:monogr/tei:imprint/tei:date', namespaces=namespace)
    
    if date_element is not None:
        # Check if 'when' attribute is present
        year = date_element.attrib.get('when', None)
        if year:
            print(f'Year of Publication: {year}')
            return
        
        # If 'when' attribute is not present, use element text
        year_text = date_element.text
        if year_text is not None:
            year_match = re.search(r'\d{4}', year_text)
            if year_match:
                print(f'Year of Publication: {year_match.group()}')
                return

    print('Year of Publication: Unknown')

# Call the function
extract_year(root, ns)

def extract_abstract(xml_root: ET.Element, namespace: dict) -> None:
    """
    This function extracts the abstract from the XML root.

    Parameters:
    xml_root (ET.Element): The root of the XML document.
    namespace (dict): The namespace for the XML document.

    Returns:
    None
    """
    abstract = xml_root.find('.//tei:profileDesc/tei:abstract', namespace)
    if abstract is not None:
        print(f'Abstract: {"".join(abstract.itertext())}')

# Call the functions
extract_title(root, ns)
extract_authors(root, ns)
extract_year(root, ns)
extract_abstract(root, ns)

# New line

