# File: src/config.py
# If using environment variables or .env file for API keys, proxies, etc.
from dotenv import load_dotenv
import os

load_dotenv()

BITQUERY_API_KEY = os.getenv("BITQUERY_API_KEY")
BITQUERY_API_URL = "https://streaming.bitquery.io/eap"

THRESHOLD = 30000

PUMPFUN_URL = "https://pump.fun/board"
PROXY = None  # Set to your proxy URL if needed