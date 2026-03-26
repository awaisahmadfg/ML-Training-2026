"""
Day 4 - APIs + Requests basics

Run:
    python3 requests_basics.py

Note:
    If your system does not have requests:
    pip install requests
"""

import requests


def get_single_post():
    # ye URL fake test API ka endpoint hai (read ke liye).
    url = "https://jsonplaceholder.typicode.com/posts/1"

    # ye GET request bhej raha hai internet par.
    response = requests.get(url, timeout=10)

    # ye line check karti hai: agar status 4xx/5xx hua to error raise karo.
    response.raise_for_status()

    # ye response body (JSON text) ko Python dict me convert karti hai.
    data = response.json()

    print("GET /posts/1 success")
    # ye line dikhati hai server ne kya status return kiya.
    print("status_code:", response.status_code)
    print("title:", data["title"])
    print("-" * 40)


def create_post():
    url = "https://jsonplaceholder.typicode.com/posts"

    # ye payload server ko bhejne wala data hai (JSON format me).
    payload = {
        "title": "Learning requests",
        "body": "This is my first POST request.",
        "userId": 1,
    }

    # json=payload automatically JSON encode + header set karta hai.
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()

    created_data = response.json()

    print("POST /posts success")
    print("status_code:", response.status_code)
    # demo API fake id return karti hai.
    print("new_id:", created_data.get("id"))
    print("-" * 40)


def request_with_params():
    url = "https://jsonplaceholder.typicode.com/comments"

    # ye query string banata hai: ?postId=1
    params = {"postId": 1}

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    comments = response.json()

    print("GET /comments?postId=1 success")
    print("count:", len(comments))
    if comments:
        print("first_email:", comments[0]["email"])
    print("-" * 40)


def auth_header_example():
    url = "https://httpbin.org/headers"

    # real APIs me token usually "Authorization: Bearer <token>" me jata hai.
    headers = {"Authorization": "Bearer demo_token_123"}

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()

    print("Custom headers example success")
    print("authorization_sent:", data["headers"].get("Authorization"))
    print("-" * 40)


def safe_request_example():
    # yahan intentionally wrong URL diya hai taaki error handling samajh aaye.
    bad_url = "https://jsonplaceholder.typicode.com/not-a-real-endpoint"

    try:
        response = requests.get(bad_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        # agar API ne not found / server error diya to yeh block chalega.
        print("HTTP error handled:", err)
    except requests.exceptions.Timeout:
        # agar request time limit me complete nahi hui.
        print("Timeout error handled")
    except requests.exceptions.RequestException as err:
        # network ya baaki generic request errors ke liye fallback.
        print("Other request error handled:", err)
    print("-" * 40)


if __name__ == "__main__":
    get_single_post()
    create_post()
    request_with_params()
    auth_header_example()
    safe_request_example()
