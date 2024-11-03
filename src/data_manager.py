import pdfplumber
import os
import pandas as pd
import itertools

# URL from which PDF to be downloaded
PDF_URL = 'https://francais-du-monde.org/wp-content/uploads/2022/11/2024-gouvernement-francais-etranger-rapport.pdf'
PDF_LOCAL_FILE = './data/2024-gouvernement-francais-etranger-rapport.pdf'
INPUT_DATA_PICKLE = './data/df.pickle'

class ReportData:
    def __init__(self):
        self.df = self.load_data()

    def get_current_location(self):
        """
        Support function to return the current directly
        :return: prints the current directory
        """
        print(os.getcwd())


    def load_data(self):
        """ Loads data from a pickle file (if exists) or from a local PDF file
         and transforms to dataframe.
         If a pickle file does not exist, then it will be created.
        :return:  with cleaned data
        """

        # Check if the file exists
        if os.path.exists(INPUT_DATA_PICKLE):
            print("Load from pickle file.")
            return pd.read_pickle(INPUT_DATA_PICKLE)

        else:
            print("Load data from local PDF and pickle.")

            # Open the PDF file and extract tables
            with pdfplumber.open(PDF_LOCAL_FILE) as pdf:

                # Extract tables using list comprehension
                # [expression for item in a list if conditional]
                pdf_tables = [page.extract_table() for page in pdf.pages if page.page_number in [151,152, 153, 154, 155]]

            # Unpack lists
            pdf_tables = list(itertools.chain(*pdf_tables))

            # Create a dataframe based on PDF table
            df = pd.DataFrame(pdf_tables[3:])
            df.columns = ['Rang', 'Country', 'Population 2023', 'Change 2023/2022 (%)', 'col1', 'col2']
            df.drop(['col1', 'col2'], axis=1, inplace=True)

            # Change datatypes
            # Rang, population in 2023; and 2023/2022 are numeric columns
            # - population : remove white space (a thousand separator)
            # - change 2023/2022: remove percentage and replace separator
            df['Population 2023'] = df['Population 2023'].str.replace(' ', '')
            df['Change 2023/2022 (%)'] = df['Change 2023/2022 (%)'].str.replace('%', '')
            df['Change 2023/2022 (%)'] = df['Change 2023/2022 (%)'].str.replace(',', '.')

            # Convert columns  to numeric
            columns_numeric = ['Rang', 'Population 2023', 'Change 2023/2022 (%)']
            df[columns_numeric] = df[columns_numeric].apply(pd.to_numeric)

            df.to_pickle(INPUT_DATA_PICKLE)

        return df
