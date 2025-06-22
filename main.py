import time, os, json, requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

WATCHLIST_FILE = "data/watchlist.txt"
STATUS_FILE = "data/status.json"

def load_watchlist():
    if not os.path.exists(WATCHLIST_FILE): return []
    with open(WATCHLIST_FILE) as f:
        return [line.strip().lower() for line in f if line.strip()]

def is_alert_enabled():
    if not os.path.exists(STATUS_FILE): return False
    with open(STATUS_FILE) as f:
        return json.load(f).get("enabled", False)

def send_telegram_message(text):
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                      data={"chat_id": TELEGRAM_CHAT_ID, "text": text})

def check_matches():
    # Replace this with live API in future
    sample = [
        {"team_a": "Team A", "team_b": "Team B", "score_a": 3, "score_b": 1, "minute": 80},
        {"team_a": "Team C", "team_b": "Team D", "score_a": 0, "score_b": 1, "minute": 60},
    ]
    watchlist = load_watchlist()
    for match in sample:
        a, b = match["team_a"].lower(), match["team_b"].lower()
        sa, sb, min = match["score_a"], match["score_b"], match["minute"]
        if min >= 75 and abs(sa - sb) >= 2:
            if any(team in (a, b) for team in watchlist):
                lead = a if sa > sb else b
                msg = f"{match['team_a']} {sa} - {sb} {match['team_b']} (min {min})\n{lead.title()} is leading by 2+ goals."
                send_telegram_message(msg)

def main():
    start = time.time()
    while time.time() - start < 12 * 3600:
        if is_alert_enabled():
            try: check_matches()
            except Exception as e: print("Error:", e)
        time.sleep(60)

if __name__ == "__main__":
    main()
