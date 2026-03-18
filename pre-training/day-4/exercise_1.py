import json
import sys

import requests


def get_json(url):
    try:
        r = requests.get(url, timeout=15)
        return r, r.json()
    except requests.exceptions.RequestException:
        return None, None
    except ValueError:
        return r, None


def print_top_repos(repos):
    repos = sorted(repos, key=lambda repo: repo.get("stargazers_count", 0), reverse=True)[:5]
    for repo in repos:
        name = repo.get("name")
        stars = repo.get("stargazers_count", 0)
        language = repo.get("language") or "Unknown"
        print(f"- {name} | ⭐ {stars} | {language}")


def main():
    username = "octocat"
    if len(sys.argv) >= 2 and sys.argv[1].strip():
        username = sys.argv[1].strip()

    profile_url = f"https://api.github.com/users/{username}"
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"

    r, profile = get_json(profile_url)
    if r is None:
        print("Network error: could not reach GitHub.", file=sys.stderr)
        return 1

    if r.status_code == 404:
        print(f"User not found: {username}", file=sys.stderr)
        return 1

    if r.status_code == 403:
        print("Rate limit hit (403). Try again later.", file=sys.stderr)
        return 1

    if r.status_code != 200 or not isinstance(profile, dict):
        print(f"Unexpected response: {r.status_code}", file=sys.stderr)
        return 1

    print("RAW JSON (profile):")
    print(json.dumps(profile, indent=2))
    print()

    r2, repos = get_json(repos_url)
    if r2 is None:
        print("Network error: could not fetch repos.", file=sys.stderr)

        return 1

    if r2.status_code == 403:
        print("Rate limit hit (403) while fetching repos. Try again later.", file=sys.stderr)
        return 1

    if r2.status_code != 200 or not isinstance(repos, list):
        print(f"Unexpected repos response: {r2.status_code}", file=sys.stderr)
        return 1

    print("RAW JSON (repos):")
    print(json.dumps(repos[:3], indent=2))
    print("... (showing first 3 repos only)")
    print()

    print("PROFILE SUMMARY")
    print("username:", profile.get("login"))
    print("bio:", profile.get("bio"))
    print("public repos:", profile.get("public_repos"))
    print("followers:", profile.get("followers"))
    print()
    print("TOP 5 REPOS BY STARS")
    print_top_repos(repos)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

