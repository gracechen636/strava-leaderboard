from flask import Flask, jsonify
import pandas as pd
import os

app = Flask(__name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/friends_data.csv")

@app.route("/")
def home():
    return "🚀 Strava Leaderboard Backend is running!"

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

if __name__ == "__main__":
    app.run(debug=True)
