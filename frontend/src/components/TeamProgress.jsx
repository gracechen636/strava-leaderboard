export default function TeamProgress({ total, goal, pct }) {
    return (
        <div className="team">
            <div className="team__header">
                <div className="team__title">Team Progress</div>
                <div className="team__value">{total.toFixed(1)} miles</div>
            </div>
            <div className="team__bar">
                <div
                    className="team__fill"
                    style={{ width: `${pct}%` }}
                />
            </div>
            <div className="team__meta">
                Team has run {Math.round(total).toLocaleString()} miles this summer —{' '}
                {Math.round(pct)}% to {goal.toLocaleString()} mi goal!
            </div>
        </div>
    );
}

