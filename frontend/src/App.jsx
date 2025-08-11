import { useEffect, useState } from 'react';

function App() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [expanded, setExpanded] = useState(null); // Tracks expanded user

  useEffect(() => {
    fetch('http://127.0.0.1:5000/leaderboard')
      .then(res => res.json())
      .then(data => {
        console.log('Fetched leaderboard:', data); // Add this
        setLeaderboard(data);
      })
      .catch(console.error);
  }, []);


  if (!leaderboard || leaderboard.length === 0) {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <h1 style={styles.heading}>Strava Leaderboard</h1>
          <p>Loading leaderboard...</p>
        </div>
      </div>
    );
  }

  const maxDistance = Math.max(...leaderboard.map(entry => entry.total_distance));

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.heading}>Strava Leaderboard</h1>

        {leaderboard.map(({ name, total_distance }) => {
          const isGrace = name.toLowerCase() === 'grace';
          const isExpanded = expanded === name;
          const percentage = (total_distance / maxDistance) * 100;

          return (
            <div
              key={name}
              onClick={() => setExpanded(expanded === name ? null : name)}
              style={{ marginBottom: '1.5rem', cursor: 'pointer' }}
            >
              <div style={styles.labelRow}>
                <span style={styles.name}>{name}</span>
                <span style={styles.miles}>
                  {total_distance.toFixed(2)} mi {isGrace ? '🏃‍♀️' : '🏃'}
                </span>
              </div>
              <div style={styles.barBackground(isExpanded)}>
                <div style={styles.barFill(percentage)} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    padding: '2rem',
    backgroundColor: '#f8f9fa',
    display: 'flex',
    justifyContent: 'center',
    fontFamily: 'Arial, sans-serif',
  },
  card: {
    backgroundColor: '#fff',
    padding: '2rem',
    borderRadius: '12px',
    boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
    width: '100%',
    maxWidth: '700px',
  },
  heading: {
    fontSize: '2.5rem',
    textAlign: 'center',
    marginBottom: '2rem',
    color: '#222',
  },
  labelRow: {
    display: 'flex',
    justifyContent: 'space-between',
    fontWeight: '600',
    marginBottom: '0.5rem',
  },
  name: {
    color: '#333',
  },
  miles: {
    color: '#666',
  },
  barBackground: (expanded) => ({
    background: '#e0e0e0',
    borderRadius: '10px',
    height: expanded ? '28px' : '16px',
    overflow: 'hidden',
    transition: 'height 0.3s',
  }),
  barFill: (percent) => ({
    height: '100%',
    width: `${percent}%`,
    background: '#4caf50',
    borderRadius: '10px',
    transition: 'width 0.4s ease-in-out',
  }),
};

export default App;
