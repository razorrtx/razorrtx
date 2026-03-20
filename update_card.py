
import os
import re
import urllib.request
import json

GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "razorrtx")
GITHUB_TOKEN = os.environ.get("GH_TOKEN", "")

SVG_TEMPLATE    = "pixel-card.svg"   
SVG_OUTPUT      = "pixel-card.svg"   



def get_contributions(username: str, token: str) -> int:
    """Ambil total contributions tahun ini via GitHub GraphQL API."""
    query = """
    query($username: String!) {
      user(login: $username) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
          }
        }
      }
    }
    """
    payload = json.dumps({"query": query, "variables": {"username": username}}).encode()

    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())

    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]


def calc_level(contributions: int) -> int:
    """Hitung level berdasarkan contributions (tiap 200 kontribusi = 1 level)."""
    return min(contributions // 200 + 1, 99)


def update_svg(username: str, contributions: int, level: int) -> None:
    """Baca template SVG dan replace placeholder dengan data asli."""
    with open(SVG_TEMPLATE, "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace("%%USERNAME%%",      username)
    content = content.replace("%%CONTRIBUTIONS%%", str(contributions))
    content = content.replace("%%LEVEL%%",         str(level))

    with open(SVG_OUTPUT, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[OK] SVG updated: {username} | contributions={contributions} | Lv {level}")


def main():
    if not GITHUB_TOKEN:
        print("[ERROR] GITHUB_TOKEN tidak ditemukan. Set di Secrets repository.")
        raise SystemExit(1)

    print(f"[INFO] Fetching data for: {GITHUB_USERNAME}")
    contributions = get_contributions(GITHUB_USERNAME, GITHUB_TOKEN)
    level         = calc_level(contributions)

    update_svg(GITHUB_USERNAME, contributions, level)


if __name__ == "__main__":
    main()
