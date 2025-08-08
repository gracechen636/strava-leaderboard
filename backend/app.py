from flask import Flask, jsonify, request
import pandas as pd
import os
from dotenv import load_dotenv
from strava import get_my_strava_data

# Initialize Flask app
app = Flask(__name__)
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# File path to the CSV file containing friends’ data
DATA_PATH     = os.path.join(os.path.dirname(__file__), "../data/friends_data.csv")
DEFAULT_START = "2025-05-01"
DEFAULT_END   = "2025-09-01"

@app.route("/exchange_token")
def exchange_token():
    """
    Endpoint to receive Strava auth code and instruct the user
    on how to manually exchange it.
    """
    code = request.args.get("code")
    return (
        "<p>Got your code!</p>"
        f"<pre>{code}</pre>"
        "<p>Copy that and then run the curl below.</p>"
    )

@app.route("/leaderboard")
def leaderboard():
    """
    Returns a JSON leaderboard combining CSV data and Grace's Strava data.
    """
    # Load the CSV
    df = pd.read_csv(DATA_PATH)

    # Drop "LAST UPDATE" column(s)
    df = df.loc[:, ~df.columns.str.contains(r"LAST\s*UPDATE", case=False)]

    # Convert all values to float (non-numeric → NaN → fill with 0.0)
    df = df.apply(pd.to_numeric, errors="coerce").fillna(0.0)

    # Sum each friend’s miles
    totals = df.sum(axis=0).to_dict()

    # Fetch Grace’s Strava data
    start = request.args.get("start", DEFAULT_START)
    end   = request.args.get("end",   DEFAULT_END)
    typ   = request.args.get("type",  None)
    my_acts = get_my_strava_data(start, end, typ)
    totals["Grace"] = sum(a["distance"] for a in my_acts)

    # Sort leaderboard
    board = sorted(totals.items(), key=lambda x: x[1], reverse=True)

    # Return JSON
    return jsonify([
        {"name": name, "total_distance": round(dist, 2)}
        for name, dist in board
    ])

if __name__ == "__main__":
    app.run(debug=True)
