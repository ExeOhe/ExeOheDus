import requests
from .config import BITQUERY_API_KEY, BITQUERY_API_URL

def get_token_supply(token_mint):
    headers = {
        "Authorization": f"Bearer {BITQUERY_API_KEY}",
        "Content-Type": "application/json"
    }

    query = {
        "query": f"""
        {{
            solana(network: solana) {{
                tokens(mintAddress: {{is: \"{token_mint}\"}}) {{
                    totalSupply
                }}
            }}
        }}
        """
    }

    response = requests.post(BITQUERY_API_URL, json=query, headers=headers)
    response.raise_for_status()
    result = response.json()

    try:
        tokens = result["data"]["solana"]["tokens"]
        if tokens and tokens[0]["totalSupply"]:
            return float(tokens[0]["totalSupply"])
    except Exception as e:
        print("Bitquery token supply response error:", e)

    return None


def get_market_caps(token_mint, since):
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

    try:
        prices = [entry["quotePrice"] for entry in result["data"]["solana"]["dexTrades"]]
        return [price * supply for price in prices]
    except Exception as e:
        print("Bitquery market cap response error:", e)

    return []
