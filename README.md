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

# 5. Run the scanner task (checks for 2x $30K pumps)
python3 -m src.main --task scan

# 6. Or run the stream task (real-time token stream)
python3 -m src.main --task stream
