import pdfplumber
import os
import pandas as pd
import itertools

# URL from which PDF to be downloaded
PDF_URL = 'https://francais-du-monde.org/wp-content/uploads/2022/11/2024-gouvernement-francais-etranger-rapport.pdf'
PDF_LOCAL_FILE = './data/2024-gouvernement-francais-etranger-rapport.pdf'

class ReportData:
    def __init__(self):
        self.load_data()

    def get_current_location(self):
        """
        Support function to return the current directly
        :return: prints the current directory
        """
        print(os.getcwd())


    def load_data(self):
        """ Loads data from local pdf file and transforms to dataframe
        :return: dataframe with data
        """

        # Open the PDF file and extract tables
        with pdfplumber.open(PDF_LOCAL_FILE) as pdf:

            # Extract tables using list comprehension
            # [ expression for item in list if conditional ]
            pdf_tables = [page.extract_table() for page in pdf.pages if page.page_number in [151,152, 153, 154, 155]]

        # Unpack lists
        pdf_tables = list(itertools.chain(*pdf_tables))

        print(pdf_tables)
        print(pdf_tables[3:])
