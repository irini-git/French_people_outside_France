import requests
import pickle

# URL from which PDF to be downloaded
PDF_URL = 'https://francais-du-monde.org/wp-content/uploads/2022/11/2024-gouvernement-francais-etranger-rapport.pdf'
FILENAME_REPORT = '../data/raw_report.pkl'

class ReportData:
    def __init__(self):
        self.load_data()

    def load_data(self):
        """
        :return:
        """

        #



