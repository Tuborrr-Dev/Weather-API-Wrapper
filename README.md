Weather API Wrapper

A FastAPI service that wraps the OpenWeatherMap free tier API. Clients call your API, your API calls theirs — clean endpoints, Pydantic validation, proper error handling, and a simple in-memory cache.

Built as a backend project covering requests, REST design, FastAPI, and Pydantic.

Features

GET /weather/{city} — returns current weather for any city by name
Geo-coding under the hood — no lat/lon required from the client
Pydantic response model — clean, typed output only
In-memory cache — skips the OpenWeatherMap API call if the same city was fetched within the last 60 seconds
Proper error handling — 400 for bad input, 404 for city not found, 502 if upstream fails, 408 on timeout