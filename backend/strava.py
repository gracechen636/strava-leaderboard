import os
import requests
from datetime import datetime
from dotenv import load_dotenv
# print("🔑 STRAVA_ACCESS_TOKEN =", os.getenv("STRAVA_ACCESS_TOKEN"))
# print("🔑 STRAVA_REFRESH_TOKEN =", os.getenv("STRAVA_REFRESH_TOKEN"))

# 1) Load environment variables from backend/.env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

CLIENT_ID       = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET   = os.getenv("STRAVA_CLIENT_SECRET")
ACCESS_TOKEN    = os.getenv("STRAVA_ACCESS_TOKEN")
REFRESH_TOKEN   = os.getenv("STRAVA_REFRESH_TOKEN")
BASE_URL        = "https://www.strava.com/api/v3"

def refresh_access_token():
    """
    If your access token has expired, use the refresh token
    to get a new access token from Strava.
    """
    resp = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id":     CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type":    "refresh_token",
            "refresh_token": REFRESH_TOKEN,
        },
    )
    resp.raise_for_status()
    data = resp.json()
    # Update in-memory tokens so subsequent calls use the fresh one
    os.environ["STRAVA_ACCESS_TOKEN"]  = data["access_token"]
    os.environ["STRAVA_REFRESH_TOKEN"] = data["refresh_token"]
    return data["access_token"]

def get_my_strava_data(start: str, end: str, activity_type: str = None):
    """
    Fetch your Strava activities between `start` and `end` dates (YYYY-MM-DD),
    optionally filtering by `activity_type` ("Run", "Ride", etc.). Returns
    a list of dicts {"name":"Grace","distance":miles,"date":"YYYY-MM-DD"}.
    """
    # 2) Parse dates and convert to epoch seconds
    after  = int(datetime.fromisoformat(start).timestamp())
    before = int(datetime.fromisoformat(end).timestamp())

    # 3) Attempt to fetch using current access token
    token   = os.getenv("STRAVA_ACCESS_TOKEN")
    headers = {"Authorization": f"Bearer {token}"}
    params  = {"after": after, "before": before, "per_page": 200}

    resp = requests.get(f"{BASE_URL}/athlete/activities", headers=headers, params=params)
    if resp.status_code == 401:
        # Token expired: refresh and retry once
        token = refresh_access_token()
        headers["Authorization"] = f"Bearer {token}"
        resp = requests.get(f"{BASE_URL}/athlete/activities", headers=headers, params=params)
    resp.raise_for_status()

    # 4) Process the JSON payload
    out = []
    for a in resp.json():
        t = a.get("type", "").lower()
        if activity_type and t != activity_type.lower():
            continue
        miles = a.get("distance", 0.0) / 1609.34
        date  = a.get("start_date_local", "").split("T")[0]
        out.append({"name": "Grace", "distance": miles, "date": date})
    return out
