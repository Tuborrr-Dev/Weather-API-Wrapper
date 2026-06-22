from fastapi import FastAPI, HTTPException, status
from requests import get, put, post, delete, Session
from pydantic import BaseModel
from dotenv import load_dotenv
import os

api_wrapper = FastAPI()
load_dotenv()
api_key = os.getenv("api_key")
"""https://api.openweathermap.org/data/4.0/onecall/current?lat={lat}&lon={lon}&appid={API key}"""
# <-- since appid is the parameter here.
"""open API url can be updated to the paid, i'm broke so i am using the free one"""
url = "https://api.openweathermap.org/data/2.5/weather"  # <- url in a variable for easy call and less messy

payload = {
    "appid": api_key,  # <-- wrapped the api in a .env file so its not shared
}


# first endpoint GET /weather/{city}
@api_wrapper.get("/weather/{city}")
def get_city(city: str):

    # we have to create api call to direct Geo-Coding
    # so we dont have our users going crazy with lon and lat in thier heads lol
    """http://api.openweathermap.org/geo/1.0/direct?q=London&limit=5&appid={API key}"""

    payload["q"] = "London"
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    """we create a session to save space"""
    with Session() as present_session:
        response = present_session.get(geo_url, params=payload)
        print(response.status_code)
        print(response.json())
        return None
