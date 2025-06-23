import requests

def discover_tokens(limit=20):
    url = "https://pumpportal.fun/api/data"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    tokens = []
    for item in data[:limit]:
        tokens.append({
            "address": item.get("token_address"),
            "name": item.get("token_name")
        })
    return tokens
