# ✅ ExeOheDus Setup (macOS/Linux)

# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. (macOS only) Fix SSL certificate errors if needed
/Applications/Python\ 3.13/Install\ Certificates.command

# 4. Set Bitquery API key (temporarily for this session)
export BITQUERY_API_KEY=your_api_key_here

* Bitquery allows up to 10,000 free API calls per month. You can monitor usage by visiting:

https://bitquery.io/user/billing

For heavy usage or production deployments, consider upgrading your Bitquery plan. *


# 5. Run the scanner task (checks for 2x $30K pumps)
python3 -m src.main --task scan

# 6. Or run the stream task (real-time token stream)
python3 -m src.main --task stream

## 📊 How Results Are Generated

- The scanner identifies tokens that have exceeded a $30,000 market cap at least twice in the last 7 days.
- For each qualifying token, the output includes up to the last 3 hourly market cap snapshots (one per hour, if available).
- This approach provides a clear, time-separated view of each asset’s recent momentum, making it easier to spot trends and analyze token performance.
- If a token has no updates for a given hour, that hour will be skipped in the results.
- Duplicate timestamps are avoided, ensuring each hourly entry is unique and actionable.

Results are saved to `pump_results.json` for further analysis or review.
