import { useEffect, useState } from 'react';

function App() {
  const [leaderboard, setLeaderboard] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/leaderboard')
      .then(res => res.json())
      .then(data => setLeaderboard(data))
      .catch(console.error);
  }, []);

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Strava Leaderboard</h1>
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Name</th>
            <th>Total Distance (mi)</th>
          </tr>
        </thead>
        <tbody>
          {leaderboard.map(({ name, total_distance }) => (
            <tr key={name}>
              <td>{name}</td>
              <td>{total_distance}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
