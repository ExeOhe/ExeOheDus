# ExeOheDus

PumpFun memecoin scraper detecting tokens that pumped above 30k twice.

## Setup (Recommended)

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
# .\venv\Scripts\activate  # On Windows
```


Install dependencies: INSIDE OF VENV

```bash
pip install -r requirements.txt
```

Run the scraper: INSIDE OF VENV

```bash
python -m src.scraper
```

The results will be saved to `pump_results.json`.

## Tests

Run unit tests with pytest:

```bash
pytest
```

## 🔐 API Key Setup

To use this tool, you'll need a free Bitquery API key.

1. Sign up at https://bitquery.io/
2. Go to your dashboard and copy your API key
3. In your terminal:

```bash
export BITQUERY_API_KEY=your_api_key_here
