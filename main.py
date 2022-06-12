import pygsheets
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager
import api_config


# This class talks to twilio
notifications = NotificationManager()
# This class talks to google sheets
google_sheet = DataManager()
# This class uses google sheet data to search for flights
flight_search = FlightSearch()
# This class processes the raw flight data
flight_data = FlightData()

# -----------Main----------- #

# Get raw flight data from API
raw_flight_data = flight_search.search_flights(google_sheet.spreadsheet_data)

# Process raw data and return a dataframe of flights found, if any
clean_flight_data = flight_data.clean_data(raw_flight_data)

# If there's flights found, send them via SMS
if len(clean_flight_data) > 0:
    notifications.send_mesg('+19192706497', clean_flight_data)


