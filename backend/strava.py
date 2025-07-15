import os
from datetime import datetime
from typing import List, Optional, Dict

import requests

BASE_URL = "https://www.strava.com/api/v3"


def _get_token(provided: Optional[str] = None) -> str:
    token = provided or os.getenv("STRAVA_ACCESS_TOKEN")
    if not token:
        raise ValueError("STRAVA_ACCESS_TOKEN not provided")
    return token


def get_my_strava_data(start: Optional[datetime] = None,
                       end: Optional[datetime] = None,
                       activity_type: Optional[str] = None,
                       access_token: Optional[str] = None) -> List[Dict]:
    """Fetch activities from the authenticated athlete's Strava account.

    Parameters
    ----------
    start : datetime, optional
        Only include activities after this time.
    end : datetime, optional
        Only include activities before this time.
    activity_type : str, optional
        Filter by activity type (e.g. "Run", "Ride").
    access_token : str, optional
        OAuth access token. If omitted, STRAVA_ACCESS_TOKEN env var is used.

    Returns
    -------
    List[Dict]
        A list of activity dictionaries with name, type, distance (km) and date.
    """
    token = _get_token(access_token)
    headers = {"Authorization": f"Bearer {token}"}

    params = {
        "page": 1,
        "per_page": 200,
    }
    if start:
        params["after"] = int(start.timestamp())
    if end:
        params["before"] = int(end.timestamp())

    activities: List[Dict] = []
    while True:
        resp = requests.get(f"{BASE_URL}/athlete/activities",
                            headers=headers,
                            params=params)
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        for act in batch:
            if activity_type and act.get("type", "").lower() != activity_type.lower():
                continue
            activities.append({
                "name": act.get("name"),
                "type": act.get("type"),
                # distances are returned in meters
                "distance": act.get("distance", 0.0) / 1000.0,
                "date": act.get("start_date_local", "")[:10],
            })
        params["page"] += 1
    return activities
