import requests
import datetime as dt

MY_CITY = "Tokyo"
MY_LAT = 35.7610122231083
MY_LON = 139.43923874808976
OWM_Endpoint = " https://api.openweathermap.org/data/2.5/forecast?"
api_key = ""


def telegram_bot_send_text(bot_message):

    bot_token = ""
    bot_chat_id = ""
    send_text = ('https://api.telegram.org/bot' +
                 bot_token +
                 '/sendMessage?chat_id=' +
                 bot_chat_id +
                 '&parse_mode=Markdown&text=' +
                 bot_message)

    bot_response = requests.get(send_text)


parameters = {
    "lat": MY_LAT,
    "lon": MY_LON,
    "cnt": 5,
    "appid": api_key
}

response = requests.get(url=OWM_Endpoint, params=parameters)
response.raise_for_status()

weather_data = response.json()

msg = ""
bring_umbrella = False

for hour_data in weather_data["list"]:

    each_hour_weather_data = hour_data["weather"][0]
    if each_hour_weather_data["id"] < 700:
        bring_umbrella = True

    # format time
    date_time = hour_data["dt_txt"]
    time_full = date_time.split(" ")[1]
    time = f"{time_full.split(':')[0]}:{time_full.split(":")[1]}"

    # Temperature
    each_hour_main_data = hour_data["main"]
    temp_in_celsius = float(hour_data["main"]["temp"]) - 273.15

    # concatenate time and description
    weather_description = each_hour_weather_data["description"]
    hourly_weather = f"{time} expect {weather_description} at {round(temp_in_celsius, 2)}°C."
    msg = f"{msg}\n{hourly_weather}"


date_now = dt.datetime.now() + dt.timedelta(hours=9)
print(date_now)
if bring_umbrella:
    msg = f"{date_now.date()}\n\nThere is a chance of rain/snow today in {MY_CITY}.\n{msg}"
else:
    msg = f"{date_now.date()}\n\nThe weather looks good today in {MY_CITY}!\n{msg}"

print(msg)
# telegram_bot_send_text(msg)



