import requests
from api_config import KIWI_API_KEY
import pandas as pd
from datetime import datetime


class FlightData:
    def __init__(self):
        pass

    # Return a dictionary of flights with prices and links
    def clean_data(self, search_results):
        clean_flights = []
        for entry in search_results:
            clean_flight = {}
            # Proceed only if there is flight data
            if self.is_flights(entry):
                clean_flight['airport_to'] = entry.json()['data'][0]['flyTo']
                clean_flight['airport_from'] = entry.json()['data'][0]['flyFrom']
                clean_flight['city_from'] = entry.json()['data'][0]['cityFrom']
                clean_flight['city_to'] = entry.json()['data'][0]['cityTo']
                clean_flight['price'] = entry.json()['data'][0]['price']
                clean_flight['purchase_link'] = entry.json()['data'][0]['deep_link']
                clean_flight['stopover_city'] = entry.json()['data'][0]['route'][0]['cityTo']
                clean_flight['departure_date'] = self.clean_date(entry.json()['data'][0]['route'][0]['local_departure'])
                clean_flight['return_date'] = self.clean_date(entry.json()['data'][0]['route'][-1]['local_arrival'])
                clean_flight['route'] = entry.json()['data'][0]['route']

                # Find all stopover cities and append to flight dictionary for each flight
                stopover_cities = []
                for route in clean_flight['route']:
                    stopover_city = route['cityTo']
                    if stopover_city == clean_flight['city_to']:
                        break
                    stopover_cities.append(stopover_city)
                clean_flight["stopover_cities"] = stopover_cities
                clean_flight["num_stopovers"] = len(clean_flight["stopover_cities"])

                clean_flights.append(clean_flight)
        return clean_flights
    
    # Ensure that data actually exists
    def is_flights(self, flight_search_results):
        if len(flight_search_results.json()['data']) == 0:
            return False
        else:
            return True

    def clean_date(self, date):
        dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f%z")
        departure_date = dt.strftime("%a, %B %d, %Y")
        return departure_date

    # Generate a purchase link using Google flights
    def generate_google_link(self, destination_airport, departure_airport, departure_date, returning_date):
        airport_to = destination_airport
        airport_from = departure_airport
        leaving_date = self.google_date(departure_date)
        return_date = self.google_date(returning_date)

        google_link = f"https://www.google.com/travel/flights?q=Flights%20to%20{airport_to}%20from%20{airport_from}%20on%{leaving_date}%20through%20{return_date}"

        return google_link

    def google_date(self,date):
        dt = datetime.strptime(date, "%a, %B %d, %Y")
        formatted_date = dt.strftime("%Y-%m-%d")
        return formatted_date