from fastapi import FastAPI, HTTPException, status
import requests
from requests import get, Session
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

cache = {}
api_wrapper = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

api_wrapper.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # this is so railway allows github pages to request
    allow_methods=["GET"],
    allow_headers=["*"],
)
load_dotenv()
api_key = os.getenv("api_key")
"""https://api.openweathermap.org/data/4.0/onecall/current?lat={lat}&lon={lon}&appid={API key}"""
# <-- since appid is the parameter here we are not using authorization
"""open API url can be updated to the paid, i'm broke so i am using the free one"""
url = "https://api.openweathermap.org/data/2.5/weather"  # <- url in a variable for easy call and less messy


class WeatherOutput(BaseModel):
    City: str
    Climate: str
    Climate_Description: str
    Temperature_in_Farheinheit: float
    Temperature_would_feel_like: float
    pressure: float
    humidity: float
    sea_level: float
    visibility: float
    wind_speed: float


# first endpoint GET /weather/{city}
@api_wrapper.get("/weather/{city}")
def get_city(city: str):
    # reject empty city call
    if city.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City name is required and cannot be empty.",
        )

    # check cache first
    if city in cache:
        cached = cache[city]
        if datetime.now() - cached["cached_at"] < timedelta(seconds=60):
            return cached["data"]

    # we have to create api call to direct Geo-Coding
    # so we dont have our users going crazy with lon and lat in thier heads lol
    """http://api.openweathermap.org/geo/1.0/direct?q=London&limit=5&appid={API key}"""
    geo_payload = {
        "q": city,
        "limit": 1,
        "appid": api_key,
    }  # <-- wrapped the api in a .env file so its not shared
    # filter out the different cities given so add limit = 1. in the first place
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    """we create a session to save space"""
    try:
        with Session() as present_session:
            geo_response = present_session.get(
                geo_url, params=geo_payload, timeout=10
            )  # <-- this is just the lat and lon cry ehn
            if not geo_response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="City not found.",
                )
            geo_response.raise_for_status()  # <-- this returns http error is there is one
            """now parse as json into a dict"""
            geo_data = geo_response.json()
            lat = geo_data[0]["lat"]
            lon = geo_data[0]["lon"]
            # now the main call
            payload = {
                "lat": lat,
                "lon": lon,
                "units": "imperial",
                "appid": api_key,
            }
            weather_response = present_session.get(url, params=payload, timeout=10)
            weather_response.raise_for_status()
            weather = weather_response.json()
            # Add Pydantic models for the request and the cleaned-up response
            final_shi = WeatherOutput(
                City=weather["name"],
                Climate=weather["weather"][0]["main"],
                Climate_Description=weather["weather"][0]["description"],
                Temperature_in_Farheinheit=weather["main"]["temp"],
                Temperature_would_feel_like=weather["main"]["feels_like"],
                pressure=weather["main"]["pressure"],
                humidity=weather["main"]["humidity"],
                sea_level=weather["main"].get("sea_level", 0.0),
                visibility=weather["visibility"],
                wind_speed=weather["wind"]["speed"],
            )
            # save data to cache
            cache[city] = {"data": final_shi, "cached_at": datetime.now()}
            return final_shi
    except requests.exceptions.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"OpenWeather API returned an error (Status {e}).",
        )
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408, detail="Request timed out")
    except requests.exceptions.RequestException as issue:
        raise HTTPException(status_code=500, detail=str(issue))
