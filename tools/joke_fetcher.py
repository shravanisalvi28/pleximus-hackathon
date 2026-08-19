"""
Joke fetcher tool — fetches a random joke from icanhazdadjoke.com.
No API key required. Returns a clean joke string.
"""

import requests

JOKE_URL = "https://icanhazdadjoke.com/"


def fetch_joke() -> str:
    """
    Fetch a random joke from icanhazdadjoke.com.

    Returns:
        A joke string, or a friendly error message.
    """
    try:
        response = requests.get(
            JOKE_URL,
            headers={"Accept": "application/json"},
            timeout=8,
        )
        response.raise_for_status()
        data = response.json()
        joke = data.get("joke", "").strip()
        if not joke:
            return "Hmm, the joke API returned nothing. Try again!"
        return joke
    except requests.exceptions.ConnectionError:
        return "Network error: Could not reach the joke service."
    except requests.exceptions.Timeout:
        return "Request timed out. The joke server is taking too long!"
    except requests.exceptions.RequestException as e:
        return f"Joke fetch failed: {e}"
