import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

#Note: use your generated data to make it work, your api_key may require few hours
# to get activated after generation so be patient and test after a while.

#api_key and end_api generated from openweathermap.org
api_key = "79f9785de0f3821f264bbeea1c3bb5a2"

#one call api
end_api = "https://api.openweathermap.org/data/3.0/onecall"

#acc_sid and auth_token generated from twilio.com
account_sid = "AC4a4fd3dd230577de25d0e330afb2ed3f"
auth_token = "1cdef436e74250ba116384cc53623aa3"

params = {
    "lat": 17.385044,
    "lon": 78.486671,
    "appid": api_key,
    "exclude": "current, minutely, daily"
}

response = requests.get(url=end_api, params=params)
response.raise_for_status()
data = response.json()
weather_data = data["hourly"][:12]

will_rain = False

for hour_data in data:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
if will_rain:
    #inorder to make the program run at specified time regularly use https://www.pythonanywhere.com/

    #to enable automation of sms at specified time on pythonanywhere using twilio
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
            #message to send as sms
            body = "It is going to rain, carry your ☔",

            #generated mobile number
            from_ = "+16184266505",

            #your verified mobile number on twilio
            to = "xxxxx12345"
    )
    print(message.status)
