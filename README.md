# PDF_Extract
get the required information as fields from PDF file    

Execution steps:

1. install packages in requirements.txt file using:
    ##### pip install -r requiremeents.txt
2. install "en_core_web_sm" model for Named Entity Recognition(NER) using:
    ##### !python -m spacy download en_core_web_sm
3. Import installed dependencies
4. finally Execute cell by cell to get output
            or
5. Run app.py file in one shot/in terminal use "python3 app.py" command
5. Create the database(I am connected to MySQL DB and using my personal credentials)
6. Use your credentials
6. check in database

###### I used Database commands in MySQL Workbench below:

create database pdf_extract_values;
use database;
show tables;
select * from pdf_data;

###### Database commands in Python

To create table:

CREATE TABLE IF NOT EXISTS pdf_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cusip_numbers TEXT,
            interest_rates TEXT,
            organizations TEXT,
            guarantors TEXT,
            metadata TEXT,
            page_num INT
        )

###### To insert values into table


INSERT INTO pdf_data (cusip_numbers, interest_rates, organizations, guarantors, metadata, page_num) VALUES (%s, %s, %s, %s, %s, %s)