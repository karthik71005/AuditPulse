import { useState } from 'react'
import { ChevronDown, ChevronUp, Copy, Check } from 'lucide-react'
import { cn } from '../lib/utils'

const IMPACT_STYLES = {
  HIGH: 'text-red-700 bg-red-50 border-red-200',
  MEDIUM: 'text-amber-700 bg-amber-50 border-amber-200',
  LOW: 'text-emerald-700 bg-emerald-50 border-emerald-200',
}
const EFFORT_STYLES = {
  LOW: 'text-indigo-700 bg-indigo-50 border-indigo-200',
  MEDIUM: 'text-amber-700 bg-amber-50/70 border-amber-200',
  HIGH: 'text-red-700 bg-red-50/70 border-red-200',
}
const STATUS_STYLES = {
  FAIL: 'border-red-200 hover:border-red-300',
  WARN: 'border-amber-200 hover:border-amber-300',
  INFO: 'border-blue-200 hover:border-blue-300',
  PASS: 'border-emerald-200 hover:border-emerald-300',
}

function CopyButton({ text }) {
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    })
  }

  return (
    <button
      onClick={handleCopy}
      className={cn(
        'flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-md border transition-all',
        copied
          ? 'text-emerald-700 bg-emerald-50 border-emerald-200'
          : 'text-blue-600 bg-blue-50 border-blue-200 hover:bg-blue-100'
      )}
    >
      {copied ? <Check size={12} /> : <Copy size={12} />}
      {copied ? 'Copied!' : 'Copy'}
    </button>
  )
}

export default function FindingCard({ finding, index }) {
  const [expanded, setExpanded] = useState(index === 0)

  return (
    <div
      className={cn(
        'bg-white border rounded-xl overflow-hidden transition-all shadow-sm hover:shadow',
        STATUS_STYLES[finding.status] || 'border-slate-200 hover:border-slate-300'
      )}
    >
      {/* Header */}
      <button
        className="w-full flex items-center justify-between gap-4 px-6 py-4 text-left hover:bg-slate-50/60 transition-colors"
        onClick={() => setExpanded((v) => !v)}
      >
        <div className="flex items-center gap-3 flex-1 min-w-0">
          <span className="text-base font-bold text-slate-900 truncate">{finding.title}</span>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          <span className={cn('text-[10px] font-bold tracking-wide uppercase px-2.5 py-1 rounded-full border', IMPACT_STYLES[finding.impact])}>
            Impact {finding.impact}
          </span>
          <span className={cn('text-[10px] font-bold tracking-wide uppercase px-2.5 py-1 rounded-full border', EFFORT_STYLES[finding.effort])}>
            Effort {finding.effort}
          </span>
          {expanded ? <ChevronUp size={16} className="text-slate-400" /> : <ChevronDown size={16} className="text-slate-400" />}
        </div>
      </button>

      {/* Body */}
      {expanded && (
        <div className="px-6 pb-5 flex flex-col gap-4 animate-fade-in border-t border-slate-100 pt-4">
          {/* Evidence */}
          <div>
            <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-1.5">Evidence</p>
            <div className="bg-slate-50 border border-slate-200 rounded-lg px-4 py-3 text-sm text-slate-700 leading-relaxed font-medium">
              {finding.evidence}
            </div>
          </div>

          {/* What to fix */}
          <div>
            <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-1.5">What to Fix</p>
            <p className="text-sm text-slate-600 leading-relaxed">{finding.description}</p>
          </div>

          {/* AI Insight */}
          {finding.ai_insight && (
            <div className="bg-blue-50/70 border border-blue-200 rounded-lg px-4 py-3.5">
              <div className="flex items-center gap-2 mb-1.5">
                <span className="text-[10px] font-bold tracking-widest uppercase text-blue-700">✦ AI Insight</span>
                <span className="text-[9px] font-bold tracking-wide uppercase px-1.5 py-0.5 rounded-full bg-blue-100 text-blue-700 border border-blue-200">
                  Groq
                </span>
              </div>
              <p className="text-sm text-slate-800 leading-relaxed font-medium">{finding.ai_insight}</p>
            </div>
          )}

          {/* Copy-paste fix */}
          {finding.copy_paste_code && (
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400">Copy-Paste Fix</p>
                <CopyButton text={finding.copy_paste_code} />
              </div>
              <pre className="bg-slate-900 border border-slate-800 rounded-lg p-4 text-xs font-mono text-emerald-400 leading-relaxed overflow-x-auto whitespace-pre-wrap break-words shadow-inner">
                {finding.copy_paste_code}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
