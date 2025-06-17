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