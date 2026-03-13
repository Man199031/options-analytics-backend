import requests
from storage import save_snapshot
from datetime import datetime

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.nseindia.com/"
}

NSE_URL = "https://www.nseindia.com/api/option-chain-indices"

def fetch_option_chain(symbol):

    # first load NSE homepage to get cookies
    session.get("https://www.nseindia.com", headers=headers)

    r = session.get(f"{NSE_URL}?symbol={symbol}", headers=headers)

    if r.status_code != 200:
        print("NSE request failed:", r.status_code)
        return None

    try:
        return r.json()
    except:
        print("Invalid JSON response")
        return None


def process_index(symbol):

    data = fetch_option_chain(symbol)

    if not data or "records" not in data:
        print("Invalid NSE response for", symbol)
        return

    rows = data["records"]["data"]

    ce_total = 0
    pe_total = 0
    strikes = []

    for r in rows:

        ce = r.get("CE")
        pe = r.get("PE")

        if ce:
            ce_total += ce["openInterest"]

        if pe:
            pe_total += pe["openInterest"]

        strikes.append({
            "strike": r["strikePrice"],
            "ce_oi": ce["openInterest"] if ce else 0,
            "pe_oi": pe["openInterest"] if pe else 0
        })

    snapshot = {
        "time": datetime.now().isoformat(),
        "ce_total": ce_total,
        "pe_total": pe_total,
        "oi_diff": pe_total - ce_total,
        "strikes": strikes
    }

    save_snapshot(symbol, snapshot)