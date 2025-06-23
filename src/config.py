# File: src/config.py
# If using environment variables or .env file for API keys, proxies, etc.
import os

PROXY = os.getenv("PUMPFUN_PROXY")
PUMPFUN_URL = "https://pump.fun/board"
THRESHOLD = 30000
