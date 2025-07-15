from flask      import Flask, jsonify, request
import pandas    as pd
import os
from dotenv import load_dotenv

from strava import get_my_strava_data

app = Flask(__name__)
load_dotenv()

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/friends_data.csv")

@app.route("/leaderboard")
def leaderboard():
    # 1. Load the pivot-style CSV
    df = pd.read_csv(DATA_PATH)

    # 2. Drop your own column and any “LAST UPDATE” column
    to_drop = []
    for col in df.columns:
        if col.strip().lower() == "grace" or col.upper().startswith("LAST UPDATE"):
            to_drop.append(col)
    df = df.drop(columns=to_drop, errors="ignore")

    # 3. Sum each remaining athlete’s column
    totals = df.sum(axis=0, skipna=True)

    # 4. Sort descending and build JSON list
    sorted_totals = totals.sort_values(ascending=False)
    result = [
        {"name": name, "total_distance": round(dist, 2)}
        for name, dist in sorted_totals.items()
    ]

    return jsonify(result)


@app.route("/combined")
def combined_leaderboard():
    """Return leaderboard including this account's Strava data."""
    df = pd.read_csv(DATA_PATH)

    to_drop = [c for c in df.columns if c.upper().startswith("LAST UPDATE")]
    df = df.drop(columns=to_drop, errors="ignore")

    totals = df.sum(axis=0, skipna=True)

    activities = get_my_strava_data()
    my_total = sum(act["distance"] for act in activities)
    totals[os.getenv("MY_NAME", "Me")] = my_total

    sorted_totals = totals.sort_values(ascending=False)
    result = [
        {"name": name, "total_distance": round(dist, 2)}
        for name, dist in sorted_totals.items()
    ]

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
