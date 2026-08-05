const PILLAR_LABELS = {
  crawlability: 'AI Bot Access',
  schema: 'Structured Schema',
  content_density: 'Answer Density',
  citations: 'Citation Share',
}

function BreakdownCard({ pillarKey, score, max }) {
  const pct = Math.round((score / max) * 100)
  const barColor =
    pct >= 70 ? '#059669' : pct >= 40 ? '#d97706' : '#dc2626'
  const scoreColor =
    pct >= 70 ? 'text-emerald-600' : pct >= 40 ? 'text-amber-600' : 'text-red-600'

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm hover:shadow-md hover:border-slate-300 transition-all">
      <p className="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-2">
        {PILLAR_LABELS[pillarKey] || pillarKey}
      </p>
      <div className="flex items-baseline gap-1 mb-3">
        <span className={`text-2xl font-extrabold ${scoreColor}`}>{score}</span>
        <span className="text-slate-400 text-sm font-normal"> / {max}</span>
      </div>
      <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-700"
          style={{ width: `${pct}%`, background: barColor }}
        />
      </div>
    </div>
  )
}

export default function BreakdownGrid({ breakdown }) {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
      {Object.entries(breakdown).map(([key, val]) => (
        <BreakdownCard key={key} pillarKey={key} score={val.score} max={val.max} />
      ))}
    </div>
  )
}
