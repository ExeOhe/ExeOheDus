import os
import requests
from .config import API_URL, THRESHOLD

API_KEY = os.getenv("MY_API_KEY")  # Set this in your environment

def fetch_tokens():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    data = response.json()
    # Filter tokens by market cap threshold
    tokens = [t for t in data if t["market_cap"] >= THRESHOLD]
    return tokens

def scrape_pumpfun():
    return fetch_tokens()

if __name__ == "__main__":
    from .storage import save_results
    tokens = scrape_pumpfun()
    save_results(tokens)
    print(f"Saved {len(tokens)} tokens")