from flask      import Flask, jsonify, request
import pandas    as pd
import os
from dotenv     import load_dotenv
from strava     import get_my_strava_data
from flask import request

@app.route("/exchange_token")
def exchange_token():
    code = request.args.get("code")
    return (
        "<p>Got your code!</p>"
        f"<pre>{code}</pre>"
        "<p>Copy that and then run the curl below.</p>"
    )

# ——————————————— Initialize Flask & load .env ———————————————
app = Flask(__name__)
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

DATA_PATH    = os.path.join(os.path.dirname(__file__), "../data/friends_data.csv")
DEFAULT_START = "2025-05-01"
DEFAULT_END   = "2025-09-01"

# ——————————————— Leaderboard Route ———————————————
@app.route("/leaderboard")
def leaderboard():
    # 1) Read the CSV
    df = pd.read_csv(DATA_PATH)

    # 2) Drop any LAST UPDATE column by name
    df = df.loc[:, ~df.columns.str.contains(r"LAST\s*UPDATE", case=False)]

    # 3) Force every value to float (non-numeric → NaN → fill with 0.0)
    df = df.apply(pd.to_numeric, errors="coerce").fillna(0.0)

    # 4) Sum each friend’s column into a plain dict
    totals = df.sum(axis=0).to_dict()  # { "Harry":200.79, ... }

    # 5) Fetch your Strava activities & sum them
    start = request.args.get("start", DEFAULT_START)
    end   = request.args.get("end",   DEFAULT_END)
    typ   = request.args.get("type",  None)  # None = all types
    my_acts = get_my_strava_data(start, end, typ)
    totals["Grace"] = sum(a["distance"] for a in my_acts)

    # 6) Sort in pure Python (no pandas!):
    board = sorted(totals.items(), key=lambda x: x[1], reverse=True)

    # 7) Return JSON
    return jsonify([{"name": n, "total_distance": round(d, 2)} for n, d in board])

# ——————————————— Run Server ———————————————
if __name__ == "__main__":
    app.run(debug=True)
