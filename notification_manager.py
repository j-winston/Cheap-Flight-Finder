import api_config
from twilio.rest import Client
import pandas as pd


# Send notification via text
class NotificationManager:
    def __init__(self):
        self.account_sid = api_config.TWILIO_SID
        self.auth_token = api_config.TWILIO_AUTH_TOKEN
        self.client = Client(username=self.account_sid, password=self.auth_token)
        self.from_number = "+19895107638"

    def send_mesg(self, to_number, cleaned_flight_data):
        # Extract message elements from DataFrame
        for row in cleaned_flight_data:
            flying_to = row['city_to']
            flying_from = row['city_from']
            price = '$' + str(row['price'])
            link = row['purchase_link']

            mesg = f"Sweet! Flight from {flying_from} to {flying_to} found for {price}. Purchase here: {link}"
            mesg_resp = self.client.messages.create(
                body=mesg,
                from_=self.from_number,
                to=to_number
            )










