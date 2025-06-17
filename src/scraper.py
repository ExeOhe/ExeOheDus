import requests
from bs4 import BeautifulSoup
from .config import PUMPFUN_URL, THRESHOLD, PROXY


def fetch_page(url: str) -> str:
    response = requests.get(url, proxies={"http": PROXY, "https": PROXY} if PROXY else None)
    response.raise_for_status()
    return response.text


def parse_pumps(html: str):
    soup = BeautifulSoup(html, "html.parser")
    # Placeholder: adapt to PumpFun's actual HTML structure
    tokens = []
    for token in soup.select("div.token"):  # Example selector
        name = token.select_one(".name").get_text(strip=True)
        pump_count = int(token.select_one(".pump-count").get_text())
        if pump_count >= 2:
            volume = int(token.select_one(".volume").get_text().replace(',', ''))
            if volume >= THRESHOLD:
                tokens.append({"name": name, "volume": volume, "pumps": pump_count})
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
