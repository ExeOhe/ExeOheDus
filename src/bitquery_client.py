import requests
from .config import BITQUERY_API_KEY, BITQUERY_API_URL
from .logic import broke_above_twice
import datetime
from collections import OrderedDict, defaultdict

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

def find_tokens_exceeding_market_cap(threshold=30000, min_times=2, since_days=30, limit=1000):
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
                # Removed PostBalanceInUSD filter to get all tokens
              }}
              orderBy: {{ descending: Block_Time }}
              limit: {{ count: {limit} }}
            ) {{
              TokenSupplyUpdate {{
                Currency {{
                    MintAddress
                    Name
                    Symbol
                }}
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
    if not updates:
        print("No updates found in Bitquery response:", result)
        return []

    since_dt = datetime.datetime.strptime(since, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
    token_counts = defaultdict(list)
    token_meta = {}  # Store metadata for each mint

    for u in updates:
        currency = u["TokenSupplyUpdate"]["Currency"]
        mint = currency["MintAddress"]
        name = currency.get("Name")
        symbol = currency.get("Symbol")
        cap = float(u["TokenSupplyUpdate"]["PostBalanceInUSD"])
        time = u.get("Block", {}).get("Time")
        if time:
            block_time_dt = datetime.datetime.fromisoformat(time.replace("Z", "+00:00"))
            if block_time_dt >= since_dt:
                token_counts[mint].append([cap, time])
                if mint not in token_meta:
                    token_meta[mint] = {"name": name, "symbol": symbol}

    results = []
    for mint, history in token_counts.items():
        # history is a list of [cap, time], so extract just the caps
        caps = [cap for cap, _ in sorted(history, key=lambda x: x[1])]
        if broke_above_twice(caps, threshold):
            hourly_history = get_last_n_hourly_market_caps(mint, n=3)
            results.append({
                "mint": mint,
                "name": token_meta[mint]["name"],
                "symbol": token_meta[mint]["symbol"],
                "history": hourly_history
            })
    return results

def get_last_n_hourly_market_caps(token_mint, n=3):
    headers = {
        "Authorization": f"Bearer {BITQUERY_API_KEY}",
        "Content-Type": "application/json"
    }
    now = datetime.datetime.now(datetime.UTC)
    since = (now - datetime.timedelta(hours=n)).strftime("%Y-%m-%dT%H:%M:%SZ")
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
              orderBy: {{ descending: Block_Time }}
              limit: {{ count: 100 }}
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
    resp = requests.post(BITQUERY_API_URL, json=query, headers=headers)
    resp.raise_for_status()
    try:
        result = resp.json()
    except Exception as e:
        print("Bitquery API did not return valid JSON:", resp.text)
        return []

    # Defensive checks
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
    # Group by hour, keep the latest per hour
    hourly_caps = OrderedDict()
    for u in sorted(updates, key=lambda x: x["Block"]["Time"], reverse=True):
        cap = float(u["TokenSupplyUpdate"]["PostBalanceInUSD"])
        ts = u["Block"]["Time"]
        dt = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
        hour_key = dt.replace(minute=0, second=0, microsecond=0)
        if hour_key not in hourly_caps:
            hourly_caps[hour_key] = [cap, ts]
        if len(hourly_caps) == n:
            break
    return list(reversed(list(hourly_caps.values())))

# Utility functions (not used by default, but kept for your reference)
def filter_history_by_interval(history, min_interval_minutes=60):
    filtered = []
    last_time = None
    for cap, ts in sorted(history, key=lambda x: x[1]):
        dt = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
        if last_time is None or (dt - last_time).total_seconds() >= min_interval_minutes * 60:
            filtered.append([cap, ts])
            last_time = dt
    return filtered

def last_n_hourly_points(history, n=3, min_interval_minutes=60):
    filtered = []
    last_time = None
    for cap, ts in sorted(history, key=lambda x: x[1], reverse=True):  # newest first
        dt = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
        if last_time is None or (last_time - dt).total_seconds() >= min_interval_minutes * 60:
            filtered.append([cap, ts])
            last_time = dt
        if len(filtered) == n:
            break
    return list(reversed(filtered))  # return oldest first

def last_n_hourly_snapshots(history, n=3):
    hourly_caps = OrderedDict()
    for cap, ts in sorted(history, key=lambda x: x[1], reverse=True):  # newest first
        dt = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
        hour_key = dt.replace(minute=0, second=0, microsecond=0)
        if hour_key not in hourly_caps:
            hourly_caps[hour_key] = [cap, ts]
        if len(hourly_caps) == n:
            break
    return list(reversed(list(hourly_caps.values())))
