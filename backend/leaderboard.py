from flask      import Flask, jsonify, request
import pandas    as pd
import os
from strava     import get_my_strava_data

app = Flask(__name__)
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/friends_data.csv")

@app.route("/leaderboard")
def leaderboard():
    # 1) Read friends' pivot CSV, keep numeric columns only
    df = pd.read_csv(DATA_PATH)
    df = df.loc[:, df.dtypes != object]

    # 2) Sum each friend
    totals = df.sum(axis=0)

    # 3) Fetch your Strava data & sum
    start = request.args.get("start")
    end   = request.args.get("end")
    typ   = request.args.get("type")
    my_acts = get_my_strava_data(start, end, typ)
    my_total = sum(a["distance"] for a in my_acts)
    totals["Grace"] = my_total   # put you back in!

    # 4) Sort descending and return JSON
    sorted_totals = totals.sort_values(ascending=False)
    result = [
        {"name": n, "total_distance": round(d, 2)}
        for n, d in sorted_totals.items()
    ]
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
