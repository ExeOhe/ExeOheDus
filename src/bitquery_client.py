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
            }}
          }}
        }}
        """
    }

    try:
        resp = requests.post(BITQUERY_API_URL, json=query, headers=headers)
        resp.raise_for_status()
        result = resp.json()

        updates = result.get("data", {}).get("TokenSupplyUpdates", [])
        if updates:
            cap = updates[0]["TokenSupplyUpdate"].get("PostBalanceInUSD")
            if cap:
                return [float(cap)]
    except Exception as e:
        print(f"Market cap fetch error for {token_mint}: {e}")

    print(f"No market cap available for {token_mint}: {result}")
    return []
