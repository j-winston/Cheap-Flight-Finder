# This class is responsible for talking to the Flight Search API.
import requests
from api_config import KIWI_API_KEY
from data_manager import DataManager
HOME_CODE = "RDU"


class FlightSearch:
    def __init__(self):
        self.search_endpoint = "https://tequila-api.kiwi.com/v2/search"
        self.search_header = {
            "apikey": KIWI_API_KEY
        }

    # Search flights for every city in the spreadsheet
    def search_flights(self, flight_spreadsheet):
        search_results = []
        # Use this to track current row of spreadsheet
        cur_row = 0
        for row in flight_spreadsheet:
            iata_code = row['IATA']
            lowest_price = row['Lowest Price']
            if iata_code is None:
                iata_code = "None Found"

            # Send this to tequila API
            search_body = {
                "fly_from": HOME_CODE,
                "fly_to": iata_code,
                "curr": 'USD',
                "price_to": lowest_price,
                "date_from": "06/06/2022",
                "date_to": "12/08/2022"
            }
            search_result = requests.get(url=self.search_endpoint,
                                          headers=self.search_header,
                                          params=search_body)
            search_results.append(search_result)
        return search_results

    #         # Check if any flights were found, if so, update spreadsheet, and print out links.
    #         if self.is_flights(search_results):
    #             city_from = search_results.json()['data'][0]['cityFrom']
    #             city_to = search_results.json()['data'][0]['cityTo']
    #             price = search_results.json()['data'][0]['price']
    #             purchase_link = search_results.json()['data'][0]['deep_link']
    #             self.data_manager.update_row(index=1, col_name='Purchase Link', value=purchase_link)
    #             # Update row number
    #             cur_row += 1
    #
    #             print(f"going from {city_from} to {city_to} with a ticket cost of {price}. You can purchase at this"
    #                   f"link: {purchase_link}")
    #         else:
    #             print(f"No flights found to {iata_code} with given constraints.")
    #
    # # Verify that flights were actually found
    # def is_flights(self, flight_search_results):
    #     if len(flight_search_results.json()['data']) == 0:
    #         return False
    #     else:
    #         return True



