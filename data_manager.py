# This class is responsible for talking to the Google Sheet.
# Import private API details
from api_config import SHEETY_USERNAME, SHEETY_AUTH_HEADER
import requests


class DataManager:
    def __init__(self):
        self.spreadsheet_endpoint = f"https://api.sheety.co/{SHEETY_USERNAME}/flightDeals/prices"
        self.spreadsheet_header = {
            "Content-Type": "application/json",
            "Authorization": SHEETY_AUTH_HEADER
        }

    def get_rows(self):
        row_data = requests.get(url=self.spreadsheet_endpoint, headers=self.spreadsheet_header)
        return row_data.json()

    def add_flight(self):
        city = input("What city would you like to go to?")
        lowest_price = input("What's the highest price you'll pay?")

        post_body = {
            "price": {
                "city": city,
                "lowestPrice": lowest_price,
                "iataCode": ""
            }
        }

        add_flight_response = requests.post(url=self.spreadsheet_endpoint,
                                            json=post_body,
                                            headers=self.spreadsheet_header)

        print(add_flight_response.text)
