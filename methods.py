"""
In this file we will extract the matherial and methods section based on the following mapping:
section_mappings = {
    'Abstract': ['Abstract', 'Summary'],
    'Introduction': ['Introduction'],
    'Methods': ['Methods', 'Methodology', 'Materials and Methods', 'Experimental Setup', 'Experimental Design', 'Experimental Procedures', 'Experimental Protocol', 'Experimental Methods', 'Experimental Section', 'Experimental', 'Study Design', 'Study Population', 'Study Sample', 'Study Participants', 'Study Protocol', 'study selection'],
    'Results': ['Results', 'Findings', 'Outcomes', 'Observations', 'Data', 'Analysis', 'Statistics'],
    'Discussion': ['Discussion', 'Interpretation', 'Implications', 'Limitations'],
    'Conclusion': ['Conclusion'],
    'Figures_Tables': ['Figures', 'Tables', 'Illustrations', 'Appendix', 'Supplementary Material'],
    'References': ['References', 'Bibliography', 'Citations', 'Sources', 'Literature Cited']
}
 But first we need to import the necessary libraries and functions
 Then check if the GROBID service is already running, and if it already running do not start it again
    Check if the GROBID service is already running
    If the request fails, it means the service is not running
    Start the GROBID service
    Wait for the GROBID service to start
    Send the PDF to GROBID
    Save the XML output
    Parse the XML output
    Define the namespace
    Parse the XML file
    Define the extract_material_and_methods function
    Find all 'div' elements in the XML
    Get the title of the section
    Check if the title contains any of the specified sections
    Print the title of the section and recursively find all 'p' elements in the 'div'
    Print the paragraph text and the text of any 'ref' elements within the paragraph
    Add a newline after the paragraph

"""

# First import the necessary modules
import subprocess
import time
import xml.etree.ElementTree as ET
import requests

section_mappings = {
    'Abstract': ['Abstract', 'Summary'],
    'Introduction': ['Introduction'],
    'Methods': ['Methods', 'Methodology', 'Materials and Methods', 'Experimental Setup', 'Experimental Design', 'Experimental Procedures', 'Experimental Protocol', 'Experimental Methods', 'Experimental Section', 'Experimental', 'Study Design', 'Study Population', 'Study Sample', 'Study Participants', 'Study Protocol', 'study selection'],
    'Results': ['Results', 'Findings', 'Outcomes', 'Observations', 'Data', 'Analysis', 'Statistics'],
    'Discussion': ['Discussion', 'Interpretation', 'Implications', 'Limitations'],
    'Conclusion': ['Conclusion'],
    'Figures_Tables': ['Figures', 'Tables', 'Illustrations', 'Appendix', 'Supplementary Material'],
    'References': ['References', 'Bibliography', 'Citations', 'Sources', 'Literature Cited']
}

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

def extract_material_and_methods(xml_root: ET.Element, namespace: dict) -> None:
    """
    This function extracts the 'Materials and Methods' section and its subheadings from the XML root.
    """
    # Find all 'div' elements in the XML
    for div in xml_root.findall('.//tei:div', namespace):
        # Get the title of the section
        title = div.find('.//tei:head', namespace)
        if title is not None:
            # If the title of the section is 'Materials and Methods' or any derivative name of 'Materials and Methods',
            # print the title and the text of the section
            if title.text in section_mappings['Methods']:
                print_section(div, namespace)

def print_section(div: ET.Element, namespace: dict) -> None:
    """
    This function prints the title and the text of a section and its subheadings.
    """
    # Print the title of the section
    title = div.find('.//tei:head', namespace)
    if title is not None:
        print(title.text)

    # Print the text of the section
    for p in div.findall('.//tei:p', namespace):
        print(p.text)
        for ref in p.findall('.//tei:ref', namespace):
            print(ref.text)
    print()

    # Recursively print the title and the text of the subheadings
    for sub_div in div.findall('.//tei:div', namespace):
        print_section(sub_div, namespace)

# Call the extract_material_and_methods function
extract_material_and_methods(root, ns)
