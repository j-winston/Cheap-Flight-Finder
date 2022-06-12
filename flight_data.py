import requests
from api_config import KIWI_API_KEY
import pandas as pd

class FlightData:
    def __init__(self):
        pass

    # Return a dictionary of flights with prices and links
    def clean_data(self, search_results):
        clean_flights = []
        cur_row = 1
        for entry in search_results:
            clean_flight = {}
            cur_row += 1
            # Proceed only if there is flight data
            if self.is_flights(entry):
                clean_flight['city_from'] = entry.json()['data'][0]['cityFrom']
                clean_flight['city_to'] = entry.json()['data'][0]['cityTo']
                clean_flight['price'] = entry.json()['data'][0]['price']
                clean_flight['purchase_link'] = entry.json()['data'][0]['deep_link']
                clean_flights.append(clean_flight)


        return clean_flights
    # Ensure that data actually exists
    def is_flights(self, flight_search_results):
        if len(flight_search_results.json()['data']) == 0:
            return False
        else:
            return True

    def print_results(self, clean_flight_data):
        if is_flights(clean_flight_data):
            for flight in clean_flight_data:
                city_from = flight['city_from']
                city_to = flight['city_to']
                price = flight['price']
                purchase_link = flight['purchase_link']

                print(f"going from {city_from} to {city_to} with a ticket cost of {price}. You can purchase at this"
                      f"link: {purchase_link}")

