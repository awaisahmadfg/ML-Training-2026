Day 4: APIs + Requests - Python talking to the world

Goal:
- To call the external API
- To understand the response (`status_code`, JSON body, headers)
- To handle the errros safely
- To work on unknown endpoints

Files:
- `day-4/requests_basics.py`
- `day-4/classes_static_class.py`
- `day-4/inheritance.py`
- `day-4/github_user_report.py`
- `day-4/weather_cli.py`

What each basic line does (core pattern):
```python
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.get(url, timeout=10)
response.raise_for_status()
data = response.json()
print(data["title"])
```

Line purpose:
- `import requests`
  - `ye library load kar raha hai` taaki HTTP requests bhej sako.
- `url = "..."`
  - `ye endpoint define kar raha hai` jahan request bhejni hai.
- `response = requests.get(url, timeout=10)`
  - `ye GET request bhej raha hai`; `timeout=10` ka matlab max 10 sec wait.
- `response.raise_for_status()`
  - `ye line yaha par status 4xx/5xx ko error me convert kar deti hai`.
- `data = response.json()`
  - `ye JSON text ko Python dict/list me badal raha hai`.
- `print(data["title"])`
  - parsed data se specific field read kar raha hai.

Most useful request patterns:
- GET with query params:
  - `requests.get(url, params={"page": 1, "limit": 20}, timeout=10)`
- POST with JSON body:
  - `requests.post(url, json={"name": "Ali"}, timeout=10)`
- Custom headers / token:
  - `requests.get(url, headers={"Authorization": "Bearer <token>"}, timeout=10)`

Error handling pattern (must know):
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.HTTPError as err:
    print("HTTP error:", err)
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.RequestException as err:
    print("Other request issue:", err)
```

How to read API docs quickly (real-world skill):
1. Check the endpoint and method (`e.g., GET /users, POST /orders`).
2. Look at the required headers (is a token or API key needed?).
3. Check the request body structure (which JSON fields are required).
4. Review response examples (both success and error responses).
5. Note rate limits and pagination details.

Exercise outputs (real API run):

1) GitHub Profile Fetcher
Run:
```bash
python3 github_user_report.py octocat
```

Example output:
```text
GitHub Report Generator

=== RAW JSON (profile) ===
{
  "login": "octocat",
  "public_repos": 8,
  "followers": 22175
  // ... bohat se aur fields ...
}

=== RAW JSON (repos preview) ===
[
  {
    "name": "hello-worId",
    "stargazers_count": 729,
    "language": null
    // ... aur fields ...
  }
]

=== GitHub User Report ===
Name: The Octocat
Username: octocat
Bio: N/A
Followers: 22175
Following: 9
Public repos: 8

Top 5 repos by stars:
- Spoon-Knife | stars: 13700 | language: HTML
- Hello-World | stars: 3546 | language: N/A
- octocat.github.io | stars: 1070 | language: CSS
- hello-worId | stars: 729 | language: N/A
- git-consortium | stars: 562 | language: N/A
```

2) Weather CLI
Run:
```bash
python3 weather_cli.py
```

Example output:
```text
Weather CLI (Open-Meteo)
Enter city name: Lahore

=== RAW JSON (geocoding result) ===
{
  "name": "Lahore",
  "latitude": 31.558,
  "longitude": 74.35071,
  "country": "Pakistan"
  // ... aur fields ...
}

=== RAW JSON (current weather) ===
{
  "temperature_2m": 22.9,
  "wind_speed_10m": 8.7,
  "weather_code": 61
  // ... aur fields ...
}

=== Current Weather ===
City: Lahore, Pakistan
Temperature: 22.9 C / 73.2 F
Wind Speed: 8.7 km/h
Description: Slight rain (code 61)
```

What was the hardest part of reading API responses?
- The GitHub API response is very large, so at first it is difficult to understand which fields are actually useful.
- In the Weather API, there are two separate responses (geocoding + forecast), and converting the weather_code into human-readable text is a bit confusing.
- Because of this, the scripts first print the raw JSON, and then extract the required data step by step.
