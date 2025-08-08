// src/components/Leaderboard.jsx
function Leaderboard({ data }) {
  return (
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Total Distance (mi)</th>
        </tr>
      </thead>
      <tbody>
        {data.map(({ name, total_distance }) => (
          <tr key={name}>
            <td>{name}</td>
            <td>{total_distance.toFixed(2)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default Leaderboard;
