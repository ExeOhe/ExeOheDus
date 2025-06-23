import argparse
from .token_filter import scrape_pumpfun
from .storage import save_results

# Main entry point for the script
# This function is called when the script is run directly
# It parses command line arguments and calls the appropriate functions
# If the task is "filter", it scrapes tokens and saves them
# It prints the number of tokens saved
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=["filter"], required=True)
    args = parser.parse_args()

    if args.task == "filter":
        tokens = scrape_pumpfun()
        save_results(tokens)
        print(f"Saved {len(tokens)} tokens")
