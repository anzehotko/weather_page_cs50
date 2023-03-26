import os
import requests
import urllib.parse
import re

from flask import redirect, render_template, request, session
from functools import wraps
from datetime import datetime, date
from collections import defaultdict


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message), code=code)


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/index")
        return f(*args, **kwargs)
    return decorated_function

def direction(degrees):
    """Convert wind direction in degrees to Cardinal Direction"""
    definition = {
        "N": [348.75, 360],
        "N": [0, 11.25],
        "NNE": [11.25, 33.75],
        "NE": [33.75, 56.25],
        "ENE": [56.25, 78.75],
        "E": [78.75, 101.25],
        "ESE": [101.25, 123.75],
        "SE": [123.75, 146.25],
        "SSE": [146.25, 168.75],
        "S": [168.75, 191.25],
        "SSW": [191.25, 213.75],
        "SW": [213.75, 236.25],
        "WSW": [236.25, 258.75],
        "W": [258.75, 281.25],
        "WNW": [281.25, 303.75],
        "NW": [303.75, 326.25],
        "NNW": [326.25, 348.75]
    }
    for key, value in definition.items():
        if value[0] <= degrees <= value[1]:
            return key
    return None





def search(city):
    """Get list of cities that have a name similar to the one searched"""

    api_key = os.environ.get("API_KEY")




    params = {
    "q": {city},
    "type": "like",
    "appid": api_key
    }

    # send the request
    response = requests.get("http://api.openweathermap.org/data/2.5/find", params=params)

    # check the status code to make sure the request was successful
    if response.status_code == 200:
        # if the request was successful, print the list of cities
        data = response.json()
        if data["list"]:
            list = data["list"]
            pr_list = []
            for i in range(len(list)):
                city = list[i]["name"]
                country = list[i]["sys"]["country"]
                pr_list.append(f"{city}, {country}")
            return pr_list
        else:
            return None






def lookup(name):
    """Look up weather data for a city."""

    api_key = os.environ.get("API_KEY")

    params = {
    "q": f"{name}",
    "units": "metric",
    "appid": api_key
    }

    # send the request
    response1 = requests.get("http://api.openweathermap.org/data/2.5/weather", params=params)

    # check the status code to make sure the request was successful
    if response1.status_code == 200:
        # if the request was successful, print the list of cities
        dtct = response1.json()

        description = dtct["weather"][0]["description"]
        icon = dtct["weather"][0]["icon"]
        link = f"http://openweathermap.org/img/wn/{icon}@2x.png"

        temperature = round((int(dtct["main"]["temp"])), 2)
        feelslike = round((int(dtct["main"]["feels_like"])), 2)
        temp_min = round((int(dtct["main"]["temp_min"])), 2)
        temp_max = round((int(dtct["main"]["temp_max"])), 2)


        pressure = dtct["main"]["pressure"]
        humidity = dtct["main"]["humidity"]
        wind_speed = dtct["wind"]["speed"]
        wind_dir = direction(dtct["wind"]["deg"])
        visibility = dtct["visibility"]



        # Getting the forecast for the specified city!

        # send the request
        response2 = requests.get("http://api.openweathermap.org/data/2.5/forecast", params=params)

        # check the status code to make sure the request was successful
        if response2.status_code == 200:
            # if the request was successful, print the list of cities
            forecast = response2.json()
            valinfo = forecast["list"]

            forecasts_by_day = defaultdict(list)
            for forecast in valinfo:
                today = date.today()
                date1 = datetime.strptime(forecast["dt_txt"], "%Y-%m-%d %H:%M:%S").date()
                weekday = date1.strftime("%A")
                stri = f"{weekday}, {date1}"
                if date1 == today:
                    pass
                else:
                    forecasts_by_day[stri].append(forecast)




            for day, listo in forecasts_by_day.items():
                min_temp = float("inf")
                max_temp = float("-inf")
                icon_12 = None
                for daytime in listo:
                    min_temp = min(min_temp, daytime["main"]["temp_min"])
                    max_temp = max(max_temp, daytime["main"]["temp_max"])
                    icon = daytime["weather"][0]["icon"]
                    noon = "12:00:00"
                    if  noon in daytime["dt_txt"]:
                        icon_12 = icon


                daily_brief = {
                    "min_temp": f"{round(min_temp, 0)} °C",
                    "max_temp": f"{round(max_temp, 0)} °C",
                    "icon_link": f"http://openweathermap.org/img/wn/{icon_12}@2x.png"
                }

                listo.append(daily_brief)





            return {
                "forecast": forecasts_by_day,
                "city": f"{name}",
                "temperature": f"{temperature} °C",
                "feelslike": f"{feelslike} °C",
                "temp_min": f"{temp_min} °C",
                "temp_max": f"{temp_max} °C",
                "pressure": f"{pressure} mBar",
                "humidity": f"{humidity} %",
                "wind_speed": f"{wind_speed} m/s",
                "wind_dir": wind_dir,
                "description": description,
                "urli": link,
                "visibility": f"{visibility} m",
            }
        else:
            return None







