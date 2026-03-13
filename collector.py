import requests
from storage import save_snapshot
from datetime import datetime

session = requests.Session()

headers = {
"User-Agent":"Mozilla/5.0",
"Accept":"application/json",
"Referer":"https://www.nseindia.com/"
}

NSE_URL="https://www.nseindia.com/api/option-chain-indices"

def fetch_option_chain(symbol):

    session.get("https://www.nseindia.com",headers=headers)

    r=session.get(f"{NSE_URL}?symbol={symbol}",headers=headers)

    return r.json()

def process_index(symbol):

    data = fetch_option_chain(symbol)

    rows = data["records"]["data"]

    ce_total=0
    pe_total=0

    strikes=[]

    for r in rows:

        ce=r.get("CE")
        pe=r.get("PE")

        if ce:
            ce_total+=ce["openInterest"]

        if pe:
            pe_total+=pe["openInterest"]

        strikes.append({
            "strike":r["strikePrice"],
            "ce_oi":ce["openInterest"] if ce else 0,
            "pe_oi":pe["openInterest"] if pe else 0
        })

    snapshot={
        "time":datetime.now().isoformat(),
        "ce_total":ce_total,
        "pe_total":pe_total,
        "oi_diff":pe_total-ce_total,
        "strikes":strikes
    }

    save_snapshot(symbol,snapshot)