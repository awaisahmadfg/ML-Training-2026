Day 4: APIs + Requests - Python talking to the world

Goal:
- External API ko call karna
- Response samajhna (`status_code`, JSON body, headers)
- Errors safely handle karna
- Docs padkar unknown endpoints pe bhi kaam karna

References:
- Corey Schafer tutorial: [youtube.com/watch?v=tb8gHvYlCFs](https://youtube.com/watch?v=tb8gHvYlCFs)
- Requests quickstart: [docs.python-requests.org/en/latest/user/quickstart](https://docs.python-requests.org/en/latest/user/quickstart/)

Files:
- `day-4/requests_basics.py`
- `day-4/github_user_report.py`
- `day-4/weather_cli.py`

Run:
```bash
cd day-4
python3 requests_basics.py
```

If requests not installed:
```bash
pip install requests
```

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
1. Endpoint + method check karo (`GET /users`, `POST /orders`).
2. Required headers dekho (token/API key?).
3. Request body shape dekho (JSON fields kaun se chahiye).
4. Response examples dekho (success + error dono).
5. Rate limits and pagination note karo.

Mini practice tasks:
1. `GET /users` call karo aur sirf names print karo.
2. `GET /posts` with `params={"userId": 1}`.
3. `POST /posts` me apna title/body bhejo.
4. Ek wrong endpoint hit karke error handler verify karo.

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
- GitHub API ka response bohat bada hota hai; pehle samajhna mushkil hota hai ke kaun se fields directly useful hain.
- Weather API me do alag responses chain hotay hain (geocoding + forecast), aur `weather_code` ko human-readable text me map karna part thora confusing hota hai.
- Is liye scripts me pehle raw JSON print kiya gaya hai, phir extraction kiya gaya hai.
