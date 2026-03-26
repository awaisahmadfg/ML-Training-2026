"""
Real API Use Case #1
GitHub User Report (Beginner Friendly)

What this script does:
- Username input leta hai
- GitHub API call karta hai
- User profile + top repos summary print karta hai
"""

import sys
import json

import requests


def fetch_user_profile(username: str) -> dict:
    # ye endpoint single user profile data deta hai.
    url = f"https://api.github.com/users/{username}"

    # ye GET request bhej raha hai; timeout lagana best practice hai.
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    # ye JSON response ko Python dict me convert karta hai.
    return response.json()


def fetch_user_repos(username: str) -> list[dict]:
    # ye endpoint user ke repos deta hai.
    url = f"https://api.github.com/users/{username}/repos"

    # params se sorting aur items limit set ki.
    params = {
        "sort": "updated",
        "per_page": 100,
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def print_report(profile: dict, repos: list[dict]) -> None:
    print("\n=== GitHub User Report ===")
    print("Name:", profile.get("name") or "N/A")
    print("Username:", profile.get("login"))
    print("Bio:", profile.get("bio") or "N/A")
    print("Followers:", profile.get("followers", 0))
    print("Following:", profile.get("following", 0))
    print("Public repos:", profile.get("public_repos", 0))

    # sirf non-fork repos filter kar rahe hain taaki meaningful projects aayein.
    own_repos = [repo for repo in repos if not repo.get("fork", False)]

    # stargazers_count ke basis pe top 5 repos.
    top_repos = sorted(
        own_repos,
        key=lambda repo: repo.get("stargazers_count", 0),
        reverse=True,
    )[:5]

    print("\nTop 5 repos by stars:")
    if not top_repos:
        print("- No repositories found")
        return

    for repo in top_repos:
        print(
            f"- {repo.get('name')} | stars: {repo.get('stargazers_count', 0)}"
            f" | language: {repo.get('language') or 'N/A'}"
        )


def print_raw_json_preview(profile: dict, repos: list[dict]) -> None:
    # pehle raw shape dekh lo, phir extraction karo.
    print("\n=== RAW JSON (profile) ===")
    print(json.dumps(profile, indent=2))

    print("\n=== RAW JSON (repos preview) ===")
    repos_preview = repos[:2]
    print(json.dumps(repos_preview, indent=2))


def get_username_from_cli_or_input() -> str:
    # bonus: agar command line argument diya hai to usay use karo.
    if len(sys.argv) > 1 and sys.argv[1].strip():
        return sys.argv[1].strip()
    return input("Enter GitHub username: ").strip()


def main() -> None:
    print("GitHub Report Generator")
    username = get_username_from_cli_or_input()

    if not username:
        print("Username empty nahi ho sakta.")
        return

    try:
        profile = fetch_user_profile(username)
        repos = fetch_user_repos(username)
        print_raw_json_preview(profile, repos)
        print_report(profile, repos)
    except requests.exceptions.HTTPError as err:
        status = err.response.status_code if err.response is not None else None

        if status == 404:
            print(f"User '{username}' not found (404). Username check karo.")
        elif status == 403:
            print(
                "GitHub rate limit hit (403). Thori der baad try karo "
                "ya authenticated request use karo."
            )
        else:
            print(f"HTTP error ({status}):", err)
    except requests.exceptions.Timeout:
        print("Request timeout - dobara try karo.")
    except requests.exceptions.RequestException as err:
        print("Network/request issue:", err)


if __name__ == "__main__":
    main()
