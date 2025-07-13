from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return "Strava Leaderboard Backend is running!"

@app.route("/leaderboard")
def leaderboard():
    # 1. Read the pivot‐style CSV: columns = athlete names, rows = distances
    df = pd.read_csv("../data/friends_data.csv")

    # 2. Sum each column (skipping any blanks/NaNs)
    totals = df.sum(axis=0, skipna=True)

    # 3. Convert to a sorted list of {name, total_distance}
    lb = (
        totals
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"index": "name", 0: "total_distance"})
    )

    # 4. Round distances and jsonify
    result = [
        {"name": row["name"], "total_distance": round(row["total_distance"], 2)}
        for _, row in lb.iterrows()
    ]
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
