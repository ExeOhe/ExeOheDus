import requests
from bs4 import BeautifulSoup
from .config import PUMPFUN_URL, THRESHOLD, PROXY


def fetch_page(url: str) -> str:
    response = requests.get(url, proxies={"http": PROXY, "https": PROXY} if PROXY else None)
    response.raise_for_status()
    return response.text


def parse_pumps(html: str):
    soup = BeautifulSoup(html, "html.parser")
    tokens = []
    for token in soup.select("div.flex.h-fit.w-full.overflow-hidden.border.p-2.group-hover\\:border-white.border-transparent.max-h-\\[300px\\].gap-2"):
        name = token.select_one(".break-anywhere.w-full.break-words.text-sm").get_text(strip=True)
        market_cap = int(token.select_one(".flex.gap-1.text-xs.text-green-300").get_text(strip=True).replace('$', '').replace(',', ''))
        if market_cap >= THRESHOLD:
            tokens.append({"name": name, "market_cap": market_cap})
    return tokens


def scrape_pumpfun():
    html = fetch_page(PUMPFUN_URL)
    tokens = parse_pumps(html)
    return tokens


if __name__ == "__main__":
    from .storage import save_results
    tokens = scrape_pumpfun()
    save_results(tokens)
    print(f"Saved {len(tokens)} tokens")
