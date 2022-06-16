             # This class is responsible for talking to the Flight Search API.
import requests
from api_config import KIWI_API_KEY
from data_manager import DataManager
from datetime import datetime, timedelta
HOME_CODE = "RDU"
from flight_data import FlightData

class FlightSearch:
    def __init__(self, stop_overs=0, via_city=''):
        self.stop_overs = 0
        self.via_city = ''
        self.search_endpoint = "https://tequila-api.kiwi.com/v2/search"
        self.search_header = {
            "apikey": KIWI_API_KEY
        }

    # Search flights for every city in the spreadsheet
    def search_flights(self, flight_spreadsheet):
        search_results = []
        
        today = datetime.today()
        date_to = today + timedelta(days=180)
        today = today.strftime("%d/%m/%Y")
        date_to = date_to.strftime("%d/%m/%Y")
        
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
                "max_stopovers": self.stop_overs,  # 0 by default
                # Departure dates
                "date_from": today,
                "date_to": date_to,
                # Returning date range
                "return_from": today,
                "return_to": date_to,
                "flight_type": "round"
                ""
            }
            search_result = requests.get(url=self.search_endpoint,
                                         headers=self.search_header,
                                         params=search_body)

            # If no direct flight is found, search with stopovers
            if len(search_result.json()['data']) == 0:
                search_body['max_stopovers'] = 2
                # search again
                search_result = requests.get(url=self.search_endpoint,
                                             headers=self.search_header,
                                             params=search_body)


            search_results.append(search_result)
        return search_results

