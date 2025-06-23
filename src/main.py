from .pumpportal_client import discover_tokens
from .bitquery_client import get_market_caps
from .logic import broke_above_twice
from .storage import save_results
from .config import THRESHOLD
import datetime
import argparse
import asyncio

# Main entry point for the script
# This function is called when the script is run directly
# It parses command line arguments and calls the appropriate functions
# If the task is "scan", it scrapes tokens and saves them
# It prints the number of tokens saved
if __name__ == "__main__":   # This block ONLY runs when you use the CLI
    parser = argparse.ArgumentParser()  # Setup CLI
    parser.add_argument("--task", choices=["scan", "stream"], required=True)
    args = parser.parse_args() # Parse the command line arguments

    if args.task == "scan":  # If user chose: --task scan
        tokens = discover_tokens(limit=20)  # <- Call the function from pumpportal_client.py

        since = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")

        results = []  # <-- Initialize results list here

        for token in tokens:
            address = token["address"]
            name = token["name"]
            try:
                history = get_market_caps(address, since)
                if broke_above_twice(history, THRESHOLD):
                    results.append({
                        "name": name,
                        "address": address,
                        "market_cap": max(history)
                    })
            except Exception as e:
                print(f"Error for {name}: {e}")

        save_results(results)
        print(f"Saved {len(results)} tokens")

    elif args.task == "stream":
        tokens = asyncio.run(stream_tokens(duration=30))
        save_results(tokens)
        print(f"Saved {len(tokens)} streamed tokens")
