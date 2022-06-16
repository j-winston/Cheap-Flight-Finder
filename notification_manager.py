import api_config
from twilio.rest import Client
import pandas as pd
import smtplib
from email.message import EmailMessage
from flight_data import FlightData

# Send notification via text
class NotificationManager:
    def __init__(self):
        self.account_sid = api_config.TWILIO_SID
        self.auth_token = api_config.TWILIO_AUTH_TOKEN
        self.client = Client(username=self.account_sid, password=self.auth_token)
        self.from_number = "+19895107638"


    # Send SMS message
    def send_mesg(self, to_number, cleaned_flight_data):
        # Extract message elements from DataFrame
        for flight_entry in cleaned_flight_data:
            city_to = flight['city_to']
            city_from = flight['city_from']
            airport_to = flight['airport_to']
            airport_from = flight['airport_from']
            departure_date = flight['departure_date']
            arrival_date = flight['arrival_date']
            price = '$' + str(row['price'])
            link = row['purchase_link']

            mesg = f"Low price alert! Only {price} to fly from {city_from}-{airport_from} to {city_to}-{airport_to}, " \
                   f"from {departure_date} to {arrival_date}."
            mesg_resp = self.client.messages.create(
                body=mesg,
                from_=self.from_number,
                to=to_number
            )

    # Send email to user list with flights
    def send_emails(self, users, flight_data):

        gmail_connection = smtplib.SMTP(host="smtp.gmail.com")
        gmail_connection.starttls()
        gmail_connection.login(user=api_config.GMAIL_USER, password=api_config.GMAIL_PASSWORD)

        # Extract email and first name
        for user in users:
            email = user['Email']
            for flight in flight_data:
                city_to = flight['city_to']
                city_from = flight['city_from']
                price = flight['price']
                link = FlightData.google_link(flight['purchase_link'])

                msg = EmailMessage()
                # Create message body
                msg.set_content(f"Low price alert! Only {price} to fly from {city_from}-{airport_from} to {city_to}-{airport_to}, " 
                                f"leaving{departure_date} and returning {return_date}.")
                msg['Subject'] = 'Cheap Flight Alert!'
                msg['From'] = 'patstevensalwayswins@gmail.com'
                msg['To'] = email

                # Send message
                gmail_connection.send_message(msg=msg)

    def print_mesg(self, flight_data):
        for flight in flight_data:
            city_to = flight['city_to']
            city_from = flight['city_from']
            airport_to = flight['airport_to']
            airport_from = flight['airport_from']
            departure_date = flight['departure_date']
            return_date = flight['return_date']
            price = '$' + str(flight['price'])
            link = flight['purchase_link']
            stopovers = flight['stopover_cities']
            num_stopovers = flight['num_stopovers']
            stopover_city = flight['stopover_cities']

            # FlightData() called just to access google link method
            # flight_data = FlightData()
            # link = flight_data.generate_google_link(airport_to, airport_from, departure_date, return_date)

            mesg = f"Low price alert! Only {price} to fly from {city_from}-{airport_from} to {city_to}-{airport_to}," \
                   f" leaving {departure_date} and returning {return_date} You can purchase here \n{link}."

            print(mesg)
            # Only if there are stopovers, display additional stopover message
            if num_stopovers > 0:
                print(f"Flight has {num_stopovers} stop over(s). Via {''.join(stopover_city)}")









