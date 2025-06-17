from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import scraper


def test_scrape_pumpfun(monkeypatch):
    html = '''
    <div class="flex h-fit w-full overflow-hidden border p-2 group-hover:border-white border-transparent max-h-[300px] gap-2">
        <span class="break-anywhere w-full break-words text-sm">FOO</span>
        <span class="flex gap-1 text-xs text-green-300">$32.0K</span>
    </div>
    '''
    monkeypatch.setattr(scraper, 'fetch_page_with_selenium', lambda url: html)
    tokens = scraper.scrape_pumpfun()
    assert tokens == [{'name': 'FOO', 'market_cap': 32000}]
