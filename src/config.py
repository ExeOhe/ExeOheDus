# File: src/config.py
# If using environment variables or .env file for API keys, proxies, etc.
import os

BITQUERY_API_KEY = os.getenv("BITQUERY_API_KEY")
BITQUERY_API_URL = "https://graphql.bitquery.io"

THRESHOLD = 30000
