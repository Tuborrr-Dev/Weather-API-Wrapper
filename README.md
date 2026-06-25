# Weather API Wrapper

A FastAPI service that wraps the OpenWeatherMap free tier API. Clients call your API, your API calls theirs — clean endpoints, Pydantic validation, proper error handling, and a simple in-memory cache.

Built as a project covering `requests`, REST design, FastAPI, and Pydantic.

---

## Features

- `GET /weather/{city}` — returns current weather for any city by name
- Geo-coding under the hood — no lat/lon required from the client
- Pydantic response model — clean, typed output only
- In-memory cache — skips the OpenWeatherMap API call if the same city was fetched within the last 60 seconds
- Proper error handling — 400 for bad input, 404 for city not found, 502 if upstream fails, 408 on timeout

---

## Stack

- **FastAPI** — server and routing
- **requests** — HTTP calls to OpenWeatherMap
- **Pydantic** — response validation and shaping
- **python-dotenv** — API key management

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/weather-api-wrapper.git
cd weather-api-wrapper
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

```
api_key=your_openweathermap_api_key_here
```

Get a free key at [openweathermap.org](https://openweathermap.org/api).  
Note: new keys can take up to 2 hours to activate.

### 4. Run the server

```bash
uvicorn main:api_wrapper --reload
```

---

## Endpoints

### `GET /weather/{city}`

Returns current weather for the given city.

**Example request:**
```
GET /weather/london
```

**Example response:**
```json
{
  "City": "London",
  "Climate": "Clouds",
  "Climate_Description": "overcast clouds",
  "Temperature_in_Farheinheit": 61.3,
  "Temperature_would_feel_like": 59.8,
  "pressure": 1012,
  "humidity": 78,
  "sea_level": 1012,
  "visibility": 10000,
  "wind_speed": 11.5
}
```

**Error responses:**

| Status | Reason |
|--------|--------|
| 400 | City name is blank |
| 404 | City not found |
| 408 | Request to OpenWeatherMap timed out |
| 502 | OpenWeatherMap returned an error |

---

## Caching

Responses are cached in memory for 60 seconds per city. A second request for the same city within that window skips the upstream API call entirely.

Cache resets on server restart.

---

## Project Structure

```
weather-api-wrapper/
├── main.py          # FastAPI app, routes, cache logic
├── .env             # API key (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## .gitignore

Make sure your `.env` is ignored:

```
.env
__pycache__/
*.pyc
```
(insight gotten from: --> )
https://roadmap.sh/projects/weather-api-wrapper-service
---
