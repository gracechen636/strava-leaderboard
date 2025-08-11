const COLORS = [
    ['#ffb703', '#ffd166'],
    ['#e5383b', '#ff7b7e'],
    ['#8e44ad', '#c39bd3'],
    ['#0077b6', '#70c3ff'],
    ['#2a9d8f', '#77d6cc'],
    ['#ef476f', '#ff9bb1'],
    ['#f77f00', '#ffb26b'],
    ['#118ab2', '#73c3df'],
];

function medalFor(rank) { if (rank === 1) return '🥇'; if (rank === 2) return '🥈'; if (rank === 3) return '🥉'; return ''; }
function runnerEmoji(name) { return name.toLowerCase() === 'grace' ? '🏃‍♀️' : '🏃'; }

export default function RunnerCard({ rank, name, miles, longest = 0, activities = [], expanded, onToggle }) {
    const [from, to] = COLORS[(rank - 1) % COLORS.length];
    const isInactive = !miles || miles < 1;

    // Compute proportional width per rank group if you prefer fixed 100% just keep as is:
    const barWidthPct = 100; // or compute relative to top if you pass max down

    // For the sparkline, clamp heights so tiny runs still show a dot
    const sparkHeights = activities.slice(-20).map(v => Math.max(8, Math.min(80, v * 6)));

    return (
        <div
            className={`card ${expanded ? 'card--expanded' : ''}`}
            onClick={onToggle}
            role="button"
            tabIndex={0}
            onKeyDown={e => (e.key === 'Enter' ? onToggle() : null)}
        >
            <div className="card__row">
                <div className="card__left">
                    <span className="card__medal">{medalFor(rank)}</span>
                    <span className="card__name">{name}</span>
                </div>
                <div className="card__right">
                    <span className="card__miles">{miles.toFixed(2)} mi</span>
                </div>
            </div>

            <div className="bar">
                <div
                    className="bar__fill"
                    style={{
                        width: `${barWidthPct}%`,
                        background: `linear-gradient(90deg, ${from}, ${to})`,
                    }}
                />
            </div>

            <div className="card__meta">
                <span className="card__emoji">{isInactive ? '🧊' : runnerEmoji(name)}</span>
                <span className="muted">
                    Longest run: {longest > 0 ? `${longest.toFixed(2)} mi` : '— mi'}
                </span>
            </div>

            {expanded && (
                <div className="expand">
                    <div className="expand__title">Activity distances</div>
                    <div className="sparkline">
                        {sparkHeights.length ? sparkHeights.map((h, i) => (
                            <div
                                key={i}
                                className="spark"
                                title={`${activities[i].toFixed ? activities[i].toFixed(2) : activities[i]} mi`}
                                style={{ height: `${h}px`, background: `linear-gradient(180deg, ${from}, ${to})` }}
                            />
                        )) : <div className="muted" style={{ padding: '8px' }}>No recent activities</div>}
                    </div>
                    <div className="expand__hint">
                        Click card to collapse.
                    </div>
                </div>
            )}
        </div>
    );
}
