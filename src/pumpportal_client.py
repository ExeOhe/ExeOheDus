# src/pumpportal_client.py
import asyncio
import websockets
import json
import time

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

async def _discover_tokens_ws(limit=20, timeout=10):
    uri = "wss://pumpportal.fun/api/data"
    tokens = []
    start = time.time()

    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({"method": "subscribeNewToken"}))

        while len(tokens) < limit and (time.time() - start) < timeout:
            try:
                data = await ws.recv()
               # print("Raw data received:", data)  # 👈 Add this line
                obj = json.loads(data)

                if "mint" in obj and "name" in obj:
                    tokens.append({
                        "mint": obj["mint"],   # or use "mint" as the key if you want
                        "name": obj["name"]
                    })

            except Exception as e:
                print(f"WebSocket error: {e}")
                break

    return tokens

def discover_tokens(limit=20, timeout=10):
    return asyncio.run(_discover_tokens_ws(limit, timeout))
# This function is a synchronous wrapper around the asynchronous _discover_tokens_ws function.
# It allows you to call discover_tokens without needing to manage the event loop directly.