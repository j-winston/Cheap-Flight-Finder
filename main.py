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
# TODO 1. Get user input
#
# print("Welcome to James' Flight Club.")
# print("We help you travel the world, on the cheap. ")
# first_name = input("What is your first name?\n")
# last_name = input("What is your last name?\n")
# email = input("What is your email address?\n")
# email_validate = input("Please type your email again.")
#
# while email != email_validate:
#     email = input("Email doesn't match. Please enter your email: ")
#     email_validate = input("Please enter your email again: ")
# print("You're in!")
#
# # Update Spreadsheet with new user
# google_sheet.add_user(first_name=first_name, last_name=last_name, email=email)

# Search for flights
raw_flight_data = flight_search.search_flights(google_sheet.spreadsheet_data)

# Process raw data and return a dict of flights, if any
clean_flight_data = flight_data.clean_data(raw_flight_data)
#
# # Get all users from spreadsheet
# users = google_sheet.get_all_users()
#
# # # TODO 3. Email all users cheap flights found
# if len(clean_flight_data) > 0:
#     notifications.alert_users(users, clean_flight_data)



notifications.print_mesg(clean_flight_data)