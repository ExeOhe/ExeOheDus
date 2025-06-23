import requests
from config import BITQUERY_API_KEY, BITQUERY_ENDPOINT

def get_market_caps(token_address, since):
    headers = {
        "X-API-KEY": BITQUERY_API_KEY,
        "Content-Type": "application/json"
    }
    query = {
        "query": f"""
        {{
            ethereum {{
                dexTrades(
                    baseCurrency: {{is: \"{token_address}\"}},
                    time: {{since: \"{since}\"}}
                ) {{
                    timeInterval {{ hour }}
                    quotePrice
                }}
            }}
        }}
        """
    }
    response = requests.post(BITQUERY_ENDPOINT, json=query, headers=headers)
    response.raise_for_status()
    result = response.json()
    return [entry["quotePrice"] for entry in result["data"]["ethereum"]["dexTrades"]]
