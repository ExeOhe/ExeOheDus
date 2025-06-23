import requests
from .config import BITQUERY_API_KEY, BITQUERY_API_URL

def get_market_caps(token_mint, since=None):
    headers = {
        "Authorization": f"Bearer {BITQUERY_API_KEY}",
        "Content-Type": "application/json"
    }

    query = {
        "query": f"""
        {{
          Solana {{
            TokenSupplyUpdates(
              where: {{
                TokenSupplyUpdate: {{
                  Currency: {{ MintAddress: {{ is: "{token_mint}" }} }}
                }}
              }}
              limit: {{ count: 1 }}
              orderBy: {{ descending: Block_Time }}
            ) {{
              TokenSupplyUpdate {{
                PostBalanceInUSD
              }}
              Block {{
                Time
              }}
            }}
          }}
        }}
        """
    }

    try:
        resp = requests.post(BITQUERY_API_URL, json=query, headers=headers)
        resp.raise_for_status()
        result = resp.json()

        updates = result.get("data", {}).get("Solana", {}).get("TokenSupplyUpdates", [])
        if updates:
            cap = updates[0]["TokenSupplyUpdate"].get("PostBalanceInUSD")
            if cap:
                return [float(cap)]
    except Exception as e:
        print(f"Market cap fetch error for {token_mint}: {e}")

    print(f"No market cap available for {token_mint}: {result}")
    return []

def find_tokens_exceeding_market_cap(threshold=30000, min_times=2, since_days=7, limit=100):
    import datetime
    headers = {
        "Authorization": f"Bearer {BITQUERY_API_KEY}",
        "Content-Type": "application/json"
    }
    since = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=since_days)).strftime("%Y-%m-%d")
    query = {
        "query": f"""
        {{
          Solana {{
            TokenSupplyUpdates(
              where: {{
                TokenSupplyUpdate: {{
                  PostBalanceInUSD: {{ gt: "{threshold}" }}
                }}
              }}
              orderBy: {{ descending: Block_Time }}
              limit: {{ count: {limit} }}
            ) {{
              TokenSupplyUpdate {{
                Currency {{ MintAddress }}
                PostBalanceInUSD
              }}
              Block {{
                Time
              }}
            }}
          }}
        }}
        """
    }
    resp = requests.post(BITQUERY_API_URL, json=query, headers=headers)
    resp.raise_for_status()
    try:
        result = resp.json()
    except Exception as e:
        print("Bitquery API did not return valid JSON:", resp.text)
        return []

    if not result or "data" not in result or result["data"] is None:
        print("Bitquery API response missing or null 'data':", result)
        return []

    if "Solana" not in result["data"] or result["data"]["Solana"] is None:
        print("Bitquery API response missing or null 'Solana':", result)
        return []

    if "TokenSupplyUpdates" not in result["data"]["Solana"]:
        print("Bitquery API response missing 'TokenSupplyUpdates':", result)
        return []

    updates = result["data"]["Solana"]["TokenSupplyUpdates"]
    from collections import defaultdict
    since_dt = datetime.datetime.strptime(since, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
    token_counts = defaultdict(list)
    for u in updates:
        mint = u["TokenSupplyUpdate"]["Currency"]["MintAddress"]
        cap = float(u["TokenSupplyUpdate"]["PostBalanceInUSD"])
        time = u.get("Block", {}).get("Time")
        if time:
            block_time_dt = datetime.datetime.fromisoformat(time.replace("Z", "+00:00"))
            if block_time_dt >= since_dt:
                token_counts[mint].append((cap, time))
    # Filter tokens that exceeded threshold at least min_times
    return [
        {"mint": mint, "history": history}
        for mint, history in token_counts.items()
        if len(history) >= min_times
    ]
