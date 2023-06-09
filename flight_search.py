import requests
from flight_data import FlightData
from pprint import pprint
import os

# Constants - can be modified to change search parameters

ADULTS = 2
NIGHTS_IN_DESTINATION_MIN = 7
NIGHTS_IN_DESTINATION_MAX = 28
FLIGHT_TYPE = "round"
MAX_STOPOVERS = 0
ONLY_WORKING_DAYS = False
ONLY_WEEKENDS = False

# Tequila constants

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = os.environ["TEQUILA_API_KEY"]


class FlightSearch:

    # Method to check for flights for a given set of inputs

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {"apikey": TEQUILA_API_KEY}
        query = {
            "adults": ADULTS,
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": NIGHTS_IN_DESTINATION_MIN,
            "nights_in_dst_to": NIGHTS_IN_DESTINATION_MAX,
            "flight_type": FLIGHT_TYPE,
            "one_for_city": 1,
            "max_stopovers": MAX_STOPOVERS,
            "curr": "USD",
            "only_working_days": ONLY_WORKING_DAYS,
            "only_weekends": ONLY_WEEKENDS
        }

        response = requests.get(
            url=f"{TEQUILA_ENDPOINT}/v2/search",
            headers=headers,
            params=query,
        )

        # Checking if the request worked with 0 stopovers

        try:
            data = response.json()["data"][0]

            # If successful, pretty print the data to the terminal

            pprint(data)

        # For destinations that can't be reached with 0 stopovers, these will cause an IndexError

        except IndexError:

            # Aiming to find a flight with the smallest number of stopovers, the request is run again with incrementing
            # stopover values until something is found

            for stopover in range(1, 12):
                try:
                    query["max_stopovers"] = stopover
                    response = requests.get(
                    url=f"{TEQUILA_ENDPOINT}/v2/search",
                    headers=headers,
                    params=query,
                )

                    # Request is checked again

                    data = response.json()["data"][0]

                    # Once a flight is found (no IndexError raised), the for loop breaks

                    break

                    # If the request raises an IndexError again, the loop continues to the next stopover increment

                except IndexError:
                    continue

            # For any instances where stopovers are necessary, details are pretty printed to terminal. Then returns data

            pprint(data)
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][1]["cityTo"],
                destination_airport=data["route"][1]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][2]["local_departure"].split("T")[0],
                stop_overs=1,
                via_city=data["route"][0]["cityTo"]
            )
            return flight_data

        # Returns initial price data for comparison with spreadsheet values

        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )

            return flight_data
