// src/services/api.js
export async function fetchLeaderboard(start, end, type) {
    const params = new URLSearchParams();
    if (start) params.append("start", start);
    if (end) params.append("end", end);
    if (type) params.append("type", type);

    const res = await fetch(`http://localhost:5000/leaderboard?${params.toString()}`);
    if (!res.ok) throw new Error("Failed to fetch leaderboard");
    return res.json();
}
