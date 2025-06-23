import requests
import os
from .config import BITQUERY_API_KEY, BITQUERY_API_URL

def get_token_supply(token_mint):
    headers = {
        "Authorization": f"Bearer {BITQUERY_API_KEY}",
        "Content-Type": "application/json"
    }
    query = {
        "query": f"""
        {{
            Solana(network: solana) {{
                TokenSupplyUpdates(
                    mintAddress: {{is: \"{token_mint}\"}}
                    limit: 1
                    orderBy: [blockHeight_desc]
                ) {{
                    supply
                }}
            }}
        }}
        """
    }
    response = requests.post(BITQUERY_API_URL, json=query, headers=headers)
    response.raise_for_status()
    result = response.json()
    if "data" not in result:
        print("Bitquery API response (get_token_supply):", result)
        return None
    tokens = result["data"]["Solana"]["TokenSupplyUpdates"]
    if tokens and tokens[0]["supply"]:
        return float(tokens[0]["supply"])
    return None

def get_market_caps(token_mint, since, interval="hour"):
    supply = get_token_supply(token_mint)
    if not supply:
        return []
    headers = {
        "Authorization": f"Bearer {BITQUERY_API_KEY}",
        "Content-Type": "application/json"
    }
    query = {
        "query": f"""
        {{
            Solana(network: solana) {{
                DEXTrades(
                    baseCurrency: {{is: \"{token_mint}\"}},
                    time: {{since: \"{since}\"}}
                ) {{
                    timeInterval {{
                        {interval}
                    }}
                    PriceInUSD
                }}
            }}
        }}
        """
    }
    response = requests.post(BITQUERY_API_URL, json=query, headers=headers)
    response.raise_for_status()
    result = response.json()
    if "data" not in result:
        print("Bitquery API response (get_market_caps):", result)
        return []
    prices = [entry["PriceInUSD"] for entry in result["data"]["Solana"]["DEXTrades"]]
    return [price * supply for price in prices]
