# create and store output values
import mysql.connector
# Parsing through PDF file
import pdfplumber
# Regular Expression to find pattern in text
import re
# To get NER like Organizations/Guarators
import spacy
# To load files from directory
import glob

# Initialize the spacy model for organization and guarantor extraction
nlp = spacy.load("en_core_web_sm")

# Define patterns for CUSIP numbers and interest rates
# cusip_pattern = r'\b[0-9A-Z]{9}\b'
cusip_pattern = r'\b\d{5}[A-Z]{3}\d{1}\b'
interest_rate_pattern = r'\d+(\.\d+)?%'
# To get organizatin names using regex
# keywords = r'\b\w+.*?(Inc|Ltd|Corporation|Corp|LLC|Bank|association|company|org|organization|pvt ltd)\b'
# organization_pattern = r'\b\w+\s\w*?\s*(?:' + keywords + r')\b'
# organization_pattern = r'\b([A-Z][a-z]+(?: [A-Z][a-z]+)* (?:|Inc\.|Ltd\.|Corporation|Corp\.|LLC\.|Bank))\b'

def extract_from_pdf(file_paths):
    data = []
    for file_path in file_paths:
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                metadata = pdf.metadata
                # Extract CUSIP numbers
                cusip_numbers = re.findall(cusip_pattern, text)
                # Extract interest rates
                interest_rates = re.findall(interest_rate_pattern, text)
                # Extract Organization without NER model
                # organizations = re.findall(organization_pattern, text)
                # Use NLP for organization names and guarantor
                doc = nlp(text)
                organizations = [ent.text for ent in doc.ents if ent.label_ == 'ORG']
                guarantors = [ent.text for ent in doc.ents if 'guarantor' in ent.sent.text.lower()]
                data.append({
                'cusip_numbers': ','.join(cusip_numbers) or None,
                'interest_rates': ','.join(interest_rates) or None,
                'organizations': ','.join(organizations) or None,
                'guarantors': ','.join(guarantors) or None,
                'metadata': str(metadata) or None,
                'page_num': page_num})
    return data


# MySQL Database connection
def connect_to_mysql():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sulochana@522",
        database="pdf_extract_values"
    )
    return connection


# Insert extracted data into MySQL
def insert_data_to_mysql(data):
    connection = connect_to_mysql()
    cursor = connection.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pdf_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cusip_numbers TEXT,
            interest_rates TEXT,
            organizations TEXT,
            guarantors TEXT,
            metadata TEXT,
            page_num INT
        )
    """)

    # Prepare SQL query
    insert_query = """
        INSERT INTO pdf_data (cusip_numbers, interest_rates, organizations, guarantors, metadata, page_num)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    for record in data:
        cursor.execute(insert_query, (
            record['cusip_numbers'],
            record['interest_rates'],
            record['organizations'],
            record['guarantors'],
            record['metadata'],
            record['page_num']
        ))

    connection.commit()
    cursor.close()
    connection.close()

## pass directory for all PDF files parse   at one time
if __name__ == "__main__":
    pdf_files = glob.glob("*.pdf")
    if len(pdf_files) == 0:
        print("No PDF files found in the directory!")
    else:
        extracted_data = extract_from_pdf(pdf_files)
        insert_data_to_mysql(extracted_data)