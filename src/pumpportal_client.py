# src/pumpportal_client.py
import asyncio
import websockets
import json
import requests

async def stream_tokens(duration=30):
    uri = "wss://pumpportal.fun/api/data"
    results = []

    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({"method": "subscribeNewToken"}))

        try:
            for _ in range(duration):
                data = await ws.recv()
                obj = json.loads(data)
                results.append(obj)
        except Exception as e:
            print(f"WebSocket error: {e}")

    return results

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
