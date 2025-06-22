from flask import Flask, render_template, request
import os, json

app = Flask(__name__)
WATCHLIST_FILE = "data/watchlist.txt"
STATUS_FILE = "data/status.json"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "watchlist" in request.files:
            f = request.files["watchlist"]
            if f.filename:
                os.makedirs("data", exist_ok=True)
                f.save(WATCHLIST_FILE)
        if "toggle" in request.form:
            set_status(not get_status())
    return render_template("index.html", enabled=get_status())

def get_status():
    if not os.path.exists(STATUS_FILE): return False
    with open(STATUS_FILE) as f:
        return json.load(f).get("enabled", False)

def set_status(val):
    os.makedirs("data", exist_ok=True)
    with open(STATUS_FILE, "w") as f:
        json.dump({"enabled": val}, f)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
