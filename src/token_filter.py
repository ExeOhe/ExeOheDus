import os
import requests
from .config import API_URL, THRESHOLD

API_KEY = os.getenv("MY_API_KEY")  # Set this in your environment

def fetch_tokens():
    headers = {"Authorization": f"Bearer {API_KEY}"} #Set the API key in the headers
    response = requests.get(API_URL, headers=headers) # Fetch data from the API URL
    response.raise_for_status() # Raise Error for bad responses w built in method
    data = response.json() # Convert response to JSON
    print(data[:5])  # Only prints the first 5 tokens
    # Filter tokens by market cap threshold
    tokens = [t for t in data if t["market_cap"] >= THRESHOLD]
    return tokens

def scrape_pumpfun():
    return fetch_tokens()

