# This class is responsible for talking to the Google Sheet.
from api_config import SHEETY_USERNAME, SHEETY_AUTH_HEADER, KIWI_API_KEY
import requests
import pygsheets


class DataManager:
    def __init__(self):
        self.gc = pygsheets.authorize(client_secret='/home/james/repos/pythonprojects/cheap_flights/client_secret.json')
        self.spreadsheet_file = self.gc.open('cheapflight')
        self.sheet_1 = self.spreadsheet_file.sheet1

        self.tequila_endpoint = "https://tequila-api.kiwi.com/locations/query"
        self.tequila_params = {
            "term": "",
            "location_types": "airport"
        }
        self.tequila_header = {
            "apikey": KIWI_API_KEY
        }

        self.spreadsheet_data = self.get_all_rows()
        self.fill_iata()

    # Return a dict of all records in flight spreadsheet
    def get_all_rows(self):
        flight_data = self.sheet_1.get_all_records()

        return flight_data

    # Check for empty IATA fields and populate with the proper airport code
    def fill_iata(self):
        row_number = 1
        for row in self.spreadsheet_data:
            row_number += 1

            if row['IATA'] == '':
                city = row['City']
                iata_code = self.find_iata(city)
                # Update spreadsheet with IATA code
                self.update_row(index=row_number, col_name='IATA', value=iata_code)

    # Get IATA airport code from tequila
    def find_iata(self, city):
        self.tequila_params["term"] = city

        request_response = requests.get(url=self.tequila_endpoint,
                                        params=self.tequila_params,
                                        headers=self.tequila_header)

        if request_response.status_code == 200:
            response_data = request_response.json()
            iata_code = response_data["locations"][0]["code"]
            return iata_code
        else:
            print("Bad request. Error occurred.")
            return 400

    def update_row(self, index, col_name, value):
        # Find the column name in the spreadsheet and also its offset
        col_offset = 0
        header = self.sheet_1[1]
        for element in header:
            # When column name is found, exit
            if element == col_name:
                break
            col_offset += 1
        # Call pygsheet method to update the spreadsheet
        self.sheet_1.update_row(index=index, values=[value], col_offset=col_offset)
        print(self.sheet_1)




