import { useRef } from 'react'
import { ExternalLink, AlertTriangle, Trophy, ArrowLeft, Zap } from 'lucide-react'
import ScoreRing from './ScoreRing'
import BreakdownGrid from './BreakdownGrid'
import FindingCard from './FindingCard'
import QueryTable from './QueryTable'
import DownloadButton from './DownloadButton'

function SectionTitle({ children }) {
  return (
    <div className="flex items-center gap-3 mb-4">
      <h2 className="text-[11px] font-bold uppercase tracking-widest text-slate-400 whitespace-nowrap">
        {children}
      </h2>
      <div className="flex-1 h-px bg-slate-200" />
    </div>
  )
}

// Sort findings: HIGH+LOW first, then HIGH+MEDIUM, then others
function sortFindings(findings) {
  const priority = (f) => {
    if (f.impact === 'HIGH' && f.effort === 'LOW') return 0
    if (f.impact === 'HIGH' && f.effort === 'MEDIUM') return 1
    if (f.impact === 'HIGH') return 2
    if (f.impact === 'MEDIUM') return 3
    return 4
  }
  return [...findings].sort((a, b) => priority(a) - priority(b))
}

export default function ReportView({ report, onReset }) {
  const reportRef = useRef(null)
  const sorted = sortFindings(report.findings || [])
  const topThree = sorted.filter((f) => f.status !== 'INFO').slice(0, 3)

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      {/* Topbar */}
      <nav className="sticky top-0 z-50 glass border-b border-slate-200 px-6 py-3.5 flex items-center justify-between no-print shadow-sm">
        <span className="text-base font-black tracking-tight text-slate-900">
          GEO<span className="text-blue-600">Auditor</span>
        </span>
        <div className="flex items-center gap-3">
          <DownloadButton report={report} reportRef={reportRef} />
          <button
            onClick={onReset}
            className="flex items-center gap-1.5 text-xs font-medium text-slate-600 hover:text-slate-900 transition-colors border border-slate-200 hover:bg-slate-100 rounded-lg px-3 py-2"
          >
            <ArrowLeft size={13} /> Audit New Site
          </button>
        </div>
      </nav>

      {/* Main content */}
      <div ref={reportRef} className="max-w-4xl mx-auto px-6 py-10">

        {/* ── Hero ─────────────────────────────────────────────────────── */}
        <div className="flex flex-wrap items-start justify-between gap-8 mb-8 bg-white border border-slate-200 rounded-2xl p-8 shadow-sm">
          <div className="flex-1 min-w-[240px]">
            <p className="text-[10px] font-bold uppercase tracking-widest text-blue-600 mb-2">
              AI Search Visibility Report
            </p>
            <h1 className="text-3xl font-black text-slate-900 mb-2 leading-tight">{report.title}</h1>
            <a
              href={report.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm font-medium text-slate-500 hover:text-blue-600 transition-colors inline-flex items-center gap-1.5"
            >
              {report.url} <ExternalLink size={12} />
            </a>
          </div>
          <ScoreRing score={report.overall_score} />
        </div>

        {/* ── Scrape warning ────────────────────────────────────────────── */}
        {report.scrape_warning && (
          <div className="flex gap-4 bg-amber-50 border border-amber-200 rounded-xl px-5 py-4 mb-6 text-amber-900">
            <AlertTriangle size={20} className="text-amber-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-bold text-amber-900 mb-1">Partial Audit — Site Blocked Scraping</p>
              <p className="text-sm text-amber-800 leading-relaxed">{report.scrape_warning}</p>
            </div>
          </div>
        )}

        {/* ── High authority notice ─────────────────────────────────────── */}
        {report.is_high_authority && (
          <div className="flex gap-4 bg-emerald-50 border border-emerald-200 rounded-xl px-5 py-4 mb-6 text-emerald-900">
            <Trophy size={20} className="text-emerald-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-bold text-emerald-900 mb-1">High-Authority Platform Detected</p>
              <p className="text-sm text-emerald-800 leading-relaxed">
                This domain is extensively cited by AI engines from training data. The score reflects{' '}
                <strong className="text-emerald-950 font-semibold">technical optimization opportunities</strong>, not actual AI visibility (which is likely much higher).
              </p>
            </div>
          </div>
        )}

        {/* ── AI Narrative ──────────────────────────────────────────────── */}
        {report.ai_narrative && (
          <div className="relative bg-gradient-to-br from-blue-50/80 via-white to-indigo-50/60 border border-blue-200 rounded-2xl px-7 py-6 mb-8 shadow-sm overflow-hidden">
            <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-600 to-violet-600" />
            <div className="flex items-center gap-2 mb-3">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-600 animate-pulse-dot" />
              <span className="text-[10px] font-bold tracking-widest uppercase text-blue-700">
                AI Executive Summary
              </span>
              <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-blue-100 text-blue-700 border border-blue-200">
                ✦ Groq · llama-3.3-70b
              </span>
            </div>
            <p className="text-[15px] leading-relaxed text-slate-800 font-medium">{report.ai_narrative}</p>
          </div>
        )}

        {/* ── Score Breakdown ───────────────────────────────────────────── */}
        <div className="mb-8">
          <SectionTitle>Score Breakdown</SectionTitle>
          <BreakdownGrid breakdown={report.breakdown} />
          {report.scoring_notes?.length > 0 && (
            <div className="flex flex-col gap-2 mt-3">
              {report.scoring_notes.map((note, i) => (
                <div
                  key={i}
                  className="bg-blue-50/70 border border-blue-200 rounded-lg px-4 py-2.5 text-xs text-blue-900 leading-relaxed font-medium"
                >
                  <span className="font-bold text-blue-700">ℹ Note: </span>{note}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* ── Buyer Queries ─────────────────────────────────────────────── */}
        <div className="mb-8">
          <SectionTitle>AI Buyer Queries Tested</SectionTitle>
          <QueryTable queries={report.buyer_queries_tested} />
        </div>

        {/* ── Findings ──────────────────────────────────────────────────── */}
        <div className="mb-8">
          <SectionTitle>Prioritized Findings</SectionTitle>
          {sorted.length === 0 ? (
            <div className="text-center py-10 bg-white border border-slate-200 rounded-2xl shadow-sm">
              <p className="text-4xl mb-3">🎉</p>
              <p className="text-emerald-700 font-bold mb-1">No critical issues found</p>
              <p className="text-sm text-slate-500">This site passed all GEO checks.</p>
            </div>
          ) : (
            <div className="flex flex-col gap-3">
              {sorted.map((finding, i) => (
                <FindingCard key={finding.check_id || i} finding={finding} index={i} />
              ))}
            </div>
          )}
        </div>

        {/* ── Monday Morning ────────────────────────────────────────────── */}
        {topThree.length > 0 && (
          <div className="bg-gradient-to-br from-slate-900 to-indigo-950 text-white rounded-2xl p-8 shadow-xl">
            <div className="flex items-center gap-2 mb-1">
              <Zap size={18} className="text-blue-400" />
              <h2 className="text-xl font-black tracking-tight text-white">What to do Monday morning</h2>
            </div>
            <p className="text-xs text-slate-400 mb-6">Highest impact, lowest effort first.</p>
            <div className="flex flex-col gap-3.5">
              {topThree.map((item, i) => (
                <div
                  key={i}
                  className="flex items-start gap-4 bg-slate-800/80 border border-slate-700/80 rounded-xl px-4 py-3.5 backdrop-blur-sm"
                >
                  <div className="w-7 h-7 rounded-full bg-gradient-to-br from-blue-500 to-violet-600 flex items-center justify-center text-xs font-black text-white flex-shrink-0 shadow">
                    {i + 1}
                  </div>
                  <div>
                    <p className="text-sm font-bold text-slate-100 mb-0.5">{item.title}</p>
                    <p className="text-xs text-slate-300 leading-relaxed">
                      {item.description.slice(0, 130)}{item.description.length > 130 ? '…' : ''}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="mt-12 pt-6 border-t border-slate-200 flex flex-wrap items-center justify-between gap-4 text-xs text-slate-400">
          <span>GEO Auditor · Checks: AI Bot Access, JSON-LD Schema, Content Structure, Citation Share</span>
          <span>Score is transparent and fully explained above</span>
        </div>
      </div>
    </div>
  )
}
