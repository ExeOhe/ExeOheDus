from .pumpportal_client import discover_tokens, stream_tokens  # <-- FIXED: added stream_tokens
from .bitquery_client import get_market_caps
from .logic import broke_above_twice
from .storage import save_results
from .config import THRESHOLD
import datetime
import argparse
import asyncio

# Main entry point for the script
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=["scan", "stream"], required=True)
    parser.add_argument("--limit", type=int, default=10)  # 👈 Add this line
    args = parser.parse_args()

    if args.task == "scan":
        tokens = discover_tokens(limit=args.limit)  # <-- Use the argument here
        since = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        results = []

        for token in tokens:
            mint = token["mint"]
            name = token["name"]
            try:
                history = get_market_caps(mint, since)  # <-- Use 'mint' instead of 'address'
                if broke_above_twice(history, THRESHOLD):
                    results.append({
                        "name": name,
                        "mint": mint,
                        "market_cap": max(history)
                    })
            except Exception as e:
                print(f"Error for {name}: {e}")

        save_results(results)
        print(f"Saved {len(results)} tokens")

    elif args.task == "stream":
        tokens = asyncio.run(stream_tokens(duration=30))  # Adjust duration if needed
        save_results(tokens)
        print(f"Saved {len(tokens)} streamed tokens")
