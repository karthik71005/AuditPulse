import { useEffect, useRef } from 'react'

export default function ScoreRing({ score }) {
  const ringRef = useRef(null)
  const circumference = 345
  const filled = Math.round((score / 100) * circumference)
  const offset = circumference - filled

  const color =
    score >= 70 ? '#059669' : score >= 45 ? '#d97706' : '#dc2626'

  const verdict =
    score >= 70 ? 'VISIBLE' : score >= 45 ? 'WEAK' : 'INVISIBLE'

  const verdictStyles = {
    VISIBLE: 'text-emerald-700 bg-emerald-50 border-emerald-200',
    WEAK: 'text-amber-700 bg-amber-50 border-amber-200',
    INVISIBLE: 'text-red-700 bg-red-50 border-red-200',
  }

  useEffect(() => {
    if (!ringRef.current) return
    ringRef.current.style.strokeDashoffset = circumference
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        if (ringRef.current) {
          ringRef.current.style.transition =
            'stroke-dashoffset 1.4s cubic-bezier(.4,0,.2,1)'
          ringRef.current.style.strokeDashoffset = offset
        }
      })
    })
  }, [score, offset])

  return (
    <div className="flex flex-col items-center gap-3 flex-shrink-0">
      <div className="relative w-36 h-36">
        <svg
          width="144"
          height="144"
          viewBox="0 0 140 140"
          style={{ transform: 'rotate(-90deg)' }}
        >
          <circle
            cx="70" cy="70" r="55"
            fill="none"
            stroke="#e2e8f0"
            strokeWidth="10"
          />
          <circle
            ref={ringRef}
            cx="70" cy="70" r="55"
            fill="none"
            stroke={color}
            strokeWidth="10"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={circumference}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-4xl font-black leading-none" style={{ color }}>
            {score}
          </span>
          <span className="text-sm text-slate-500 font-medium">/100</span>
        </div>
      </div>
      <span
        className={`text-xs font-bold tracking-widest uppercase px-3 py-1 rounded-full border ${verdictStyles[verdict]}`}
      >
        {verdict}
      </span>
    </div>
  )
}
