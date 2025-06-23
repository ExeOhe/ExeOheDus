# src/pumpportal_client.py
import asyncio
import websockets
import json

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
