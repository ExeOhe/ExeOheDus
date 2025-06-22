import argparse
from token_filter import scrape_pumpfun
from storage import save_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=["filter"], required=True)
    args = parser.parse_args()

    if args.task == "filter":
        tokens = scrape_pumpfun()
        save_results(tokens)
        print(f"Saved {len(tokens)} tokens")
