# strava-leaderboard
A custom leaderboard tracker for my friend group’s Strava-based run/walk/hike competitions. Since Strava’s leaderboard resets weekly, this tool allows us to define a custom competition period (e.g., May 1–Aug 1) and automatically calculate total activity stats over that range, eliminating manual tracking.

## Setup

1. Install the Python dependencies:

   ```bash
   pip install -r backend/requirements.txt
   ```

2. Copy `.env.example` to `.env` and provide your Strava access token.

3. Ensure `data/friends_data.csv` contains your friends' distances in a pivot
   format (columns are friend names, rows are distances for each day).

4. Start the Flask server:

   ```bash
   python backend/app.py
   ```

## Endpoints

- `GET /leaderboard` – totals from the CSV file only.
- `GET /combined` – the CSV totals plus your own Strava activity totals.
