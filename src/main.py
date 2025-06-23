import argparse
import asyncio
import datetime

from .pumpportal_client import discover_tokens, stream_tokens
from .bitquery_client import get_market_caps, find_tokens_exceeding_market_cap
from .logic import broke_above_twice
from .storage import save_results
from .config import THRESHOLD

# Main entry point for the script
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=["scan", "stream"], required=True)
    parser.add_argument("--limit", type=int, default=1000)
    args = parser.parse_args()

    if args.task == "scan":
        results = find_tokens_exceeding_market_cap(
            threshold=THRESHOLD,
            min_times=2,
            since_days=7,
            limit=args.limit  # or higher if you want to scan more
        )
        save_results(results)
        print(f"Saved {len(results)} tokens")

    elif args.task == "stream":
        tokens = asyncio.run(stream_tokens(duration=30))
        save_results(tokens)
        print(f"Saved {len(tokens)} streamed tokens")
