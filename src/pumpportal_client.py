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

async def _discover_tokens_ws(limit=20):
    uri = "wss://pumpportal.fun/api/data"
    tokens = []

    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({"method": "subscribeNewToken"}))

        while len(tokens) < limit:
            try:
                data = await ws.recv()
                obj = json.loads(data)

                if "token_address" in obj and "token_name" in obj:
                    tokens.append({
                        "address": obj["token_address"],
                        "name": obj["token_name"]
                    })

            except Exception as e:
                print(f"WebSocket error: {e}")
                break

    return tokens

def discover_tokens(limit=20):
    return asyncio.run(_discover_tokens_ws(limit))
# This function is a synchronous wrapper around the asynchronous _discover_tokens_ws function.
# It allows you to call discover_tokens without needing to manage the event loop directly.