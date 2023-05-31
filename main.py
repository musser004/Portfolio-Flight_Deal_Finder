from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

# Constants

ORIGIN_CITY_IATA = "AVL"

# Module classes are called

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# Data pulled in from Google Sheets via Sheety API

sheet_data = data_manager.get_destination_data()

# Dictionary comprehension for destinations info

destinations = {data["iataCode"]: {
        "id": data["id"],
        "city": data["city"],
        "price": data["priceThreshold"]
    } for data in sheet_data}

# Datetime setup for tomorrow and 6 month from today dates (search parameters for finding flights)

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=182)

# Main loop. Goes through the full list of destination iata codes and checks for applicable flights

for destination_code in destinations:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination_code,
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    # Ignore and continue the loop if None is returned

    if flight is None:
        continue

    # If flight price is found to be lower than price threshold in spreadsheet, email message is sent to list of users

    if flight.price < destinations[destination_code]["price"]:

        # Flight info is

        # Name and email lists are created with list comprehension

        users = data_manager.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]

        # Message is defined with flight data

        message = f"Low price alert! Only ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to" \
                  f" {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to" \
                  f" {flight.return_date}."

        # If the flight contains any stopovers, an additional line is added to the message

        if flight.stop_overs > 0:
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

        notification_manager.send_emails(emails, message)

        # Phone message is sent

        notification_manager.send_sms(message)
