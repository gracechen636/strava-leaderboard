import { useEffect, useMemo, useState } from 'react';
import RunnerCard from './components/RunnerCard.jsx';
import TeamProgress from './components/TeamProgress.jsx';
import './index.css';

const API = 'http://127.0.0.1:5000/leaderboard';

export default function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState(null);

  useEffect(() => {
    fetch(API)
      .then(r => r.json())
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const team = useMemo(() => {
    const total = data.reduce((s, x) => s + (x.total_distance || 0), 0);
    const goal = 2000;
    const pct = goal ? Math.min(100, (total / goal) * 100) : 0;
    return { total, goal, pct };
  }, [data]);

  return (
    <div className="page">
      <div className="container">
        <h1 className="title">Strava Leaderboard</h1>
        {loading && <p className="muted">Loading leaderboard…</p>}

        {!loading && (
          <>
            <div className="grid">
              {data.map((row, i) => (
                <RunnerCard
                  key={row.name}
                  rank={i + 1}
                  name={row.name}
                  miles={row.total_distance}
                  longest={row.longest}            // NEW
                  activities={row.activities || []} // NEW (last 20)
                  expanded={expanded === row.name}
                  onToggle={() => setExpanded(expanded === row.name ? null : row.name)}
                />
              ))}
            </div>

            <TeamProgress total={team.total} goal={team.goal} pct={team.pct} />
          </>
        )}
      </div>
    </div>
  );
}
