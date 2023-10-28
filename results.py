# In this file we will only extract the results from the pdf extraction based on the xml file generated by grobid. 
import subprocess
import time
import xml.etree.ElementTree as ET
from typing import Any
import requests


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

def extract_results(xml_root: ET.Element, namespace: dict) -> None:
    """
    This function extracts the results section from the XML root.

    Parameters:
    xml_root (ET.Element): The root of the XML document.
    namespace (dict): The namespace for the XML document.

    Returns:
    None
    """
    # Flag to indicate whether we are in the 'results' section
    in_results = False

    # Find all 'div' elements in the XML
    for div in xml_root.findall('.//tei:div', namespace):
        # Get the title of the section
        title = div.find('tei:head', ns)
        if title is not None:
            title = title.text.strip().lower()  # Remove leading/trailing whitespace and convert to lower case

            # Check if the title contains 'results'
            if 'results' in title:
                print('Results section found:\n')
                in_results = True

            # If we are in the 'results' section and encounter a 'div' with 'discussion' or 'conclusion' in the title, stop printing
            if in_results and ('discussion' in title or 'conclusion' in title):
                break

        if in_results:
            # Print the title of the subsection
            if title and 'results' not in title:
                print(title)

            # Recursively find all 'p' elements in the 'div'
            paragraphs = div.findall('.//tei:p', ns)
            for paragraph in paragraphs:
                if paragraph is not None:  # Check if the paragraph exists
                    # Print the paragraph text
                    print(paragraph.text, end='')  # Don't add a newline after the paragraph text

                    # Print the text of any 'ref' elements within the paragraph
                    for ref in paragraph.findall('.//tei:ref', ns):
                        if ref.text:
                            print(ref.text, end='')  # Don't add a newline after the reference text

                    print()  # Add a newline after the paragraph

def extract_tables(xml_root: Any, namespace: Any) -> None:
    """
    This function extracts all tables from the XML root.

    Parameters:
    xml_root (Any): The root of the XML document.
    namespace (Any): The namespace for the XML document.

    Returns:
    None
    """
    # Find all 'figure' elements in the XML
    for figure in xml_root.findall('.//tei:figure', namespace):
        table = figure.find('.//tei:table', ns)
        if table is not None:
            print("\nTable:")
            rows = table.findall('.//tei:row', ns)
            for row in rows:
                cells = [cell.text for cell in row.findall('.//tei:cell', ns) if cell.text]
                print('\t'.join(cells))

# Call the functions
extract_results(root, ns)
extract_tables(root, ns)

# Add a newline at the end of the file

