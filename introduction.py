import os
import subprocess
import time
import xml.etree.ElementTree as ET
import requests

# Path to the GROBID service
GROBID_PATH = '/Users/franciscoteixeirabarbosa/projects/test/sections_pdf/grobid'

def extract_introduction(PDF_PATH: str, namespace: dict = None) -> str:
    """
    This function extracts the introduction from the XML root.

    Parameters:
    PDF_PATH (str): The path to the PDF document.
    namespace (dict): The namespace for the XML document.

    Returns:
    str: The extracted introduction text.
    """
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
    except requests.exceptions.RequestException:
        # If the request fails, it means the service is not running
        print("GROBID service is not running. Starting it now...")
        subprocess.Popen(['./gradlew', 'run', '--stacktrace'], cwd=GROBID_PATH)
        # Wait for the GROBID service to start
        time.sleep(10)
    
    if namespace is None:
        namespace = {'tei': 'http://www.tei-c.org/ns/1.0'}

    # Send the PDF to GROBID
    with open(PDF_PATH, 'rb') as f:
        response = requests.post('http://localhost:8070/api/processFulltextDocument', files={'input': f}, timeout=10)

    # Save the XML output
    with open('output.xml', 'w', encoding='utf-8') as f:
        f.write(response.text)

    # Parse the XML output
    tree = ET.parse('output.xml')
    root = tree.getroot()

    # Mapping dictionary to associate various section names with generalized names
    section_mappings = {
        'Introduction': ['introduction', 'summary', 'background', 'background and aims', 'background and purpose', 'background and objective', 'background and objectives', 'background and rationale', 'background and significance', 'background information', 'context', 'context and background', 'context and objective', 'context and objectives', 'context and rationale', 'context and significance', 'context and study design', 'context and study objective', 'context and study objectives', 'context and study rationale', 'context and study significance', 'context a'],
    }

    previous_section = None

    # Find all 'div' elements in the XML
    for div in root.findall('.//tei:div', namespace):
        # Get the title of the section
        title = div.find('tei:head', namespace)
        if title is not None:
            title = title.text.strip().lower()  # Remove leading/trailing whitespace and convert to lower case

            # Check if the title contains any of the specified sections
            for section, variants in section_mappings.items():
                if any(variant in title for variant in variants):
                    print(f'\n{section}:\n')
                    
                    # If the methods section is found, return the previous section as the introduction
                    if section == 'methods':
                        return previous_section

                    # Get the paragraphs of the section
                    paragraphs = [''.join(p.itertext()) for p in div.findall('.//tei:p', namespace)]
                    full_text = ' '.join(paragraphs)
                    print(full_text)

                    # Store the current section as the previous section
                    previous_section = full_text

    # If no methods section is found, return None
    return None

print(extract_introduction('/Users/franciscoteixeirabarbosa/projects/test/sections_pdf/data/Implant_abutment interface_ biomechanical study of flat top versus conical.pdf'))