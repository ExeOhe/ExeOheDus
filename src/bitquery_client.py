import requests
from .config import BITQUERY_API_KEY, BITQUERY_API_URL

def get_market_caps(token_mint, since):
    headers = {
        "X-API-KEY": BITQUERY_API_KEY,
        "Content-Type": "application/json"
    }
    query = {
        "query": f"""
        {{
            solana(network: solana) {{
                dexTrades(
                    baseCurrency: {{is: \"{token_mint}\"}},
                    time: {{since: \"{since}\"}}
                ) {{
                    timeInterval {{ hour }}
                    quotePrice
                }}
            }}
        }}
        """
    }
    response = requests.post(BITQUERY_API_URL, json=query, headers=headers)
    response.raise_for_status()
    result = response.json()
    return [entry["quotePrice"] for entry in result["data"]["solana"]["dexTrades"]]
