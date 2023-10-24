import subprocess
import time
import os
import requests
import xml.etree.ElementTree as ET

# Path to the GROBID service
grobid_path = '/Users/franciscoteixeirabarbosa/projects/test/sections_pdf/grobid'

# Start the GROBID service
p = subprocess.Popen(['./gradlew', 'run', '--stacktrace'], cwd=grobid_path)

# Wait for the GROBID service to start
time.sleep(10)

pdf_path = '/Users/franciscoteixeirabarbosa/projects/test/sections_pdf/data/IMPACT_OF_VARIOUS_IMPRESSION_TECHNIQUES.pdf'

# Send the PDF to GROBID
with open(pdf_path, 'rb') as f:
    response = requests.post('http://localhost:8070/api/processFulltextDocument', files={'input': f})

# Save the XML output
with open('output.xml', 'w') as f:
    f.write(response.text)

# Parse the XML output
tree = ET.parse('output.xml')
root = tree.getroot()

# Mapping dictionary to associate various section names with generalized names
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

tree = ET.parse('/Users/franciscoteixeirabarbosa/projects/test/sections_pdf/grobid/output.xml')
root = tree.getroot()

# Define the namespace
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

# Find all 'div' elements in the XML
for div in root.findall('.//tei:div', ns):
    # Get the title of the section
    title = div.find('tei:head', ns).text if div.find('tei:head', ns) is not None else 'No title'
    title = title.strip().lower()  # Remove leading/trailing whitespace and convert to lower case
    print(f'Processing section: {title}')  # Debug print
    
    # Check if the title contains any of the specified sections
    for section, variants in section_mappings.items():
        variants = [variant.lower() for variant in variants]  # Convert variants to lower case
        if any(variant in title for variant in variants):
            print(f'Match found for section: {section}')  # Debug print
            
            print(f'\n{section}:\n')
            
            # Get the paragraphs of the section
            paragraphs = [p.text for p in div.findall('tei:p', ns)]
            print('\n'.join(paragraphs))