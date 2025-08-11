from flask import Flask, jsonify, request
import pandas as pd
import os
from dotenv import load_dotenv
from strava import get_my_strava_data
from flask_cors import CORS
import math

# Initialize Flask app
app = Flask(__name__)
CORS(app)
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

DATA_PATH     = os.path.join(os.path.dirname(__file__), "../data/friends_data.csv")
DEFAULT_START = "2025-05-01"
DEFAULT_END   = "2025-09-01"


def _series_to_activities_and_longest(series, limit=20):
    """
    Given a pandas Series of numbers (one person's column),
    return (activities_list, longest_value).
    - activities_list: last `limit` non-null values, in chronological order.
    - longest_value: max of non-null values (0.0 if none).
    """
    s = pd.to_numeric(series, errors="coerce").dropna()
    longest = float(s.max()) if len(s) else 0.0
    # last 20 non-empty entries (treat as separate activities)
    last_vals = s.tail(limit).tolist()
    # ensure floats
    acts = [float(x) for x in last_vals]
    return acts, longest


@app.route("/leaderboard")
def leaderboard():
    """
    Returns a JSON leaderboard with totals +
    details for each person:
      - total_distance (sum)
      - longest (max single entry/run in miles)
      - activities (last up-to-20 distances)
    Grace's details/activities come from Strava. Others from the CSV.
    """
    # 1) Load CSV and clean
    df = pd.read_csv(DATA_PATH)
    df = df.loc[:, ~df.columns.str.contains(r"LAST\s*UPDATE", case=False)]
    df = df.apply(pd.to_numeric, errors="coerce")

    # 2) Get date/type filters
    start = request.args.get("start", DEFAULT_START)
    end   = request.args.get("end",   DEFAULT_END)
    typ   = request.args.get("type",  None)

    # 3) Base totals from CSV (sum columns)
    totals = df.sum(axis=0, skipna=True).to_dict()
    # make sure all totals are floats
    totals = {k: float(v) for k, v in totals.items()}

    # 4) Build per-person details from CSV
    details = {}
    for name in df.columns:
        acts, longest = _series_to_activities_and_longest(df[name], limit=20)
        details[name] = {
            "activities": acts,
            "longest": float(longest),
        }

    # 5) Grace from Strava (override CSV totals AND details)
    my_acts = get_my_strava_data(start, end, typ)  # list of {name, distance, date}
    grace_distances = [float(a["distance"]) for a in my_acts]
    totals["Grace"] = float(sum(grace_distances))
    grace_longest = float(max(grace_distances)) if grace_distances else 0.0
    # Keep last 20 activities, chronological order (oldest->newest)
    # Strava usually returns newest first; reverse to chronological for sparkline feel
    grace_last20 = grace_distances[-20:]
    details["Grace"] = {
        "activities": grace_last20,
        "longest": grace_longest,
    }

    # 6) Compose list and sort by total descending
    board = []
    for name, total in totals.items():
        board.append({
            "name": name,
            "total_distance": round(float(total), 2),
            "longest": round(float(details.get(name, {}).get("longest", 0.0)), 2),
            "activities": [round(float(x), 2) for x in details.get(name, {}).get("activities", [])],
        })

    board.sort(key=lambda x: x["total_distance"], reverse=True)

    return jsonify(board)


if __name__ == "__main__":
    app.run(debug=True)
