# Project: Flight Deal Finder Application (Python Scripting)

Demo video: https://youtu.be/_QDx6nvFBAY

Description: Using various API's, application checks a spreadsheet for flight destination information, then checks for deals with a given set of adjustable options. If a deal is found (lower than the adjustable price threshold listed in the spreadsheet), an email/text message updates is sent out to the list of users.

Python Libraries: Requests, Smtplib, Datetime, OS

NOTE: Application requires environmental variables (not included) in order to run properly

# How to use:

1.) Ideally, create your own google sheets document. Then, create an account with Sheety

https://dashboard.sheety.co/

Create a new project, then link the spreadsheet to that project

2.) For the google sheets document:

- Add a tab named "prices". Within this tab, set up 3 column titles as "City", "IATA Code", and "Price Threshold", respectively
- Add a tab named "users". WIthin this tab, set up 3 column titles as "First Name", "Last Name", and "Email"
- On the "prices" tab, add in locations you'd like to fly to, along with their IATA code
- In the "Price Threshold" column, add in the maximum price that you'd be willing to pay to fly out there (this is what will determine whether or not you will receive an alert from a flight found via the search)
- On the "users" tab, add in contact information for whoever you want to receive the alerts

3.) Set up environmental  variables for notification_manager.py

- Set up a twilio account + phone number. Add in environmental variables for: "TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", and "TWILIO_PHONE_NUM"
- Add in "DESTINATION_PHONE", "MY_GMAIL", and "APP_PASSWORD" (the latter being the app password for gmail)

4.) Set up environmental variables for data_manager.py:

NOTE: "SHEETY_APP_ID" and "SHEETY_APP_KEY" should be given during account setup

NOTE: "SHEETY_AUTHORIZATION" will require you to do the additional step on the sheety website of setting up authorization for that particular project (if you see the 3 tabs "API", "Authentication", "Settings" on the project page, select "Authentication". I went with a bearer token)

NOTE: "SHEETY_ENDPOINT" and "USER_ENDPOINT" are important for pulling the data from the google sheets document. These will be the "GET" API links that sheety will show in that project, on that sheet (there should be 2 sheets - one for "prices, and one for "users")

5.) Set up environmental variables for flight_search.py:

Set up account with Tequila API here:

https://tequila.kiwi.com/portal/login

Then add environmental variables for "TEQUILA_ENDPOINT" and "TEQUILA_API_KEY"

6.) Adjust the constants at the top of flight_search.py as desired. These will modify the search parameters

7.) Adjust the "ORIGIN_CITY_IATA" constant in main.py to be whatever airport IATA code that you want to fly out from. You can also comment out the current "start" and "end" variables, then uncomment the manual date controls below that to select what dates you'd like to use as the start/end range for DEPARTURE flight dates in the search

8.) Run the program. If everything is set up properly, you should be getting pretty printed terminal readouts, along with text and email messages sent. Messages should include price, origin city/destination city, dates, and a link to the deal
