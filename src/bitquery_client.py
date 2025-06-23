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
              where: {{ TokenSupplyUpdate: {{ Currency: {{ MintAddress: {{ is: \"{token_mint}\" }} }} }} }}
              limit: {{ count: 1 }}
              orderBy: {{ descending: Block_Time }}
            ) {{
              TokenSupplyUpdate {{ PostBalanceInUSD }}
            }}
          }}
        }}
        """
    }

    resp = requests.post(BITQUERY_API_URL, json=query, headers=headers)
    resp.raise_for_status()
    result = resp.json()

    if "data" not in result or not result["data"].get("Solana") or not result["data"]["Solana"].get("TokenSupplyUpdates"):
        print(f"No market cap available for {token_mint}: {result}")
        return []

    cap_usd = result["data"]["Solana"]["TokenSupplyUpdates"][0]["TokenSupplyUpdate"]["PostBalanceInUSD"]
    return [float(cap_usd)]
