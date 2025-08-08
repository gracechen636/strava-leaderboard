from flask      import Flask, jsonify, request
import pandas    as pd
import os
from strava     import get_my_strava_data

app = Flask(__name__)
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/friends_data.csv")

@app.route("/leaderboard")
def leaderboard():
    # 1) Load the CSV
    df = pd.read_csv(DATA_PATH)

    # 2) Drop any "LAST UPDATE" column by name (case‑insensitive)
    drop_mask = df.columns.str.contains("LAST\s*UPDATE", case=False)
    df = df.loc[:, ~drop_mask]

    # 3) Coerce all data to numbers, turning non-numeric into NaN
    df = df.apply(pd.to_numeric, errors="coerce")

    # 4) Sum each column (friends)
    totals = df.sum(axis=0, skipna=True).to_dict()

    # 5) Fetch & sum your Strava miles for May 1→Sep 1 2025 by default
    start = request.args.get("start", "2025-05-01")
    end   = request.args.get("end",   "2025-09-01")
    typ   = request.args.get("type",  None)  # None => all activity types
    my_acts = get_my_strava_data(start, end, typ)
    totals["Grace"] = sum(a["distance"] for a in my_acts)

    # 6) Sort in Python so we never mix dtypes in numpy
    items = [(name, float(dist)) for name, dist in totals.items()]
    items.sort(key=lambda x: x[1], reverse=True)

    # 7) Return as JSON
    return jsonify([
        {"name": name, "total_distance": round(dist, 2)}
        for name, dist in items
    ])

if __name__ == "__main__":
    app.run(debug=True)
