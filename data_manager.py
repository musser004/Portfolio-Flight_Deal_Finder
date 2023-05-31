import requests
import os

# Environmental variables are pulled in

SHEETY_APP_ID = os.environ["SHEETY_APP_ID"]
SHEETY_API_KEY = os.environ["SHEETY_APP_KEY"]
SHEETY_AUTHORIZATION = os.environ["SHEETY_AUTHORIZATION"]
SHEETY_PRICES_ENDPOINT = os.environ["SHEETY_ENDPOINT"]
SHEETY_USERS_ENDPOINT = os.environ["USER_ENDPOINT"]

# Headers defined for authorization purposes

sheety_headers = {
    "x-app-id": SHEETY_APP_ID,
    "x-app-key": SHEETY_API_KEY,
    "Authorization": SHEETY_AUTHORIZATION
}


class DataManager:

    def __init__(self):
        self.destination_data = {}

    # Method to pull destination data from "prices" tab of spreadsheet

    def get_destination_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, headers=sheety_headers)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    # Method to pull user information from "users" tab of spreadsheet

    def get_customer_emails(self):
        customers_endpoint = SHEETY_USERS_ENDPOINT
        response = requests.get(url=customers_endpoint, headers=sheety_headers)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data
