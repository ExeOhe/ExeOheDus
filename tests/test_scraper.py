from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import scraper


def test_scrape_pumpfun(monkeypatch):
    html = '''
    <div class="token"><span class="name">FOO</span><span class="pump-count">2</span><span class="volume">32000</span></div>
    <div class="token"><span class="name">BAR</span><span class="pump-count">1</span><span class="volume">50000</span></div>
    '''
    monkeypatch.setattr(scraper, 'fetch_page', lambda url: html)
    tokens = scraper.scrape_pumpfun()
    assert tokens == [{'name': 'FOO', 'volume': 32000, 'pumps': 2}]
