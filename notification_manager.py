import smtplib
from twilio.rest import Client
import os

# Environmental variables and constants are defined

TWILIO_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_VIRTUAL_NUMBER = os.environ["TWILIO_PHONE_NUM"]
TWILIO_VERIFIED_NUMBER = os.environ["DESTINATION_PHONE"]
MAIL_PROVIDER_SMTP_ADDRESS = "smtp.gmail.com"
MY_EMAIL = os.environ["MY_GMAIL"]
MY_PASSWORD = os.environ["APP_PASSWORD"]


class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    # Method to send text message to verified phone number (environmental variable) via Twilio API

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
        )

    # Method to send email via smtplib

    def send_emails(self, emails, message):
        with smtplib.SMTP(MAIL_PROVIDER_SMTP_ADDRESS) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)

            # Set to work with a list of emails (pulled from spreadsheet)

            for email in emails:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}".encode('utf-8')
                )
