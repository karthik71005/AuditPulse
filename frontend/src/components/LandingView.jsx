import { useState } from 'react'
import { Search, Bot, FileCode2, BarChart3, Link2 } from 'lucide-react'

const CHECKS = [
  { icon: Bot, label: 'AI bot crawlability' },
  { icon: FileCode2, label: 'JSON-LD schema markup' },
  { icon: BarChart3, label: 'Content answer density' },
  { icon: Link2, label: 'Live citation presence' },
]

const STEPS = [
  '🌐 Crawling your site…',
  '🤖 Checking AI bot access…',
  '📐 Analysing structured schema…',
  '🔍 Testing live citation share…',
  '✦ Generating AI insights…',
]

export default function LandingView({ onAudit, isLoading }) {
  const [url, setUrl] = useState('')
  const [currentStep, setCurrentStep] = useState(0)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!url.trim()) return
    // Animate loading steps
    let step = 0
    const interval = setInterval(() => {
      step++
      setCurrentStep(step)
      if (step >= STEPS.length - 1) clearInterval(interval)
    }, 2000)
    onAudit(url.trim())
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 py-16 relative overflow-hidden bg-slate-50">
      {/* Background glow */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-1/4 left-1/5 w-[600px] h-[400px] bg-blue-500/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/3 right-1/5 w-[500px] h-[350px] bg-violet-500/10 rounded-full blur-3xl" />
      </div>

      {/* Header pill */}
      <div className="flex items-center gap-2 text-[11px] font-bold tracking-widest uppercase text-blue-700 bg-blue-50 border border-blue-200 px-4 py-1.5 rounded-full mb-8 shadow-sm">
        <span className="w-1.5 h-1.5 rounded-full bg-blue-600 animate-pulse-dot" />
        Generative Engine Optimization
      </div>

      {/* Hero */}
      <h1 className="text-5xl font-black text-center leading-tight tracking-tight max-w-2xl mb-5 text-slate-900">
        Is your business{' '}
        <span className="text-gradient">invisible to AI search?</span>
      </h1>
      <p className="text-lg text-slate-600 text-center max-w-xl mb-12 leading-relaxed">
        Most businesses rank on Google but get{' '}
        <strong className="text-slate-900 font-semibold">zero mentions</strong> in ChatGPT,
        Perplexity, and Google AI Overviews. Find out where you stand.
      </p>

      {/* Form card */}
      <div className="w-full max-w-xl bg-white border border-slate-200 shadow-xl shadow-slate-200/50 rounded-2xl p-8 relative overflow-hidden">
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-600 to-violet-600" />

        <form onSubmit={handleSubmit}>
          <label className="block text-[11px] font-bold uppercase tracking-widest text-slate-500 mb-2.5">
            Your website URL
          </label>
          <div className="flex gap-2.5">
            <input
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              type="text"
              placeholder="https://yoursite.com"
              disabled={isLoading}
              className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm text-slate-900 placeholder-slate-400 outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition-all disabled:opacity-50 font-medium"
            />
            <button
              type="submit"
              disabled={isLoading || !url.trim()}
              className="flex items-center gap-2 bg-gradient-to-r from-blue-600 to-violet-600 text-white font-bold px-6 py-3 rounded-xl text-sm hover:shadow-lg hover:shadow-blue-500/25 active:scale-95 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:scale-100 whitespace-nowrap"
            >
              <Search size={15} />
              {isLoading ? 'Auditing…' : 'Audit →'}
            </button>
          </div>
        </form>

        {/* Loading steps */}
        {isLoading && (
          <div className="mt-6 flex flex-col gap-2 animate-fade-in">
            <div className="w-6 h-6 border-2 border-slate-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-2" />
            {STEPS.map((step, i) => (
              <div
                key={i}
                className={`flex items-center gap-2.5 text-sm font-medium transition-colors ${
                  i < currentStep
                    ? 'text-emerald-600'
                    : i === currentStep
                    ? 'text-slate-900'
                    : 'text-slate-400'
                }`}
              >
                <span>{i < currentStep ? '✓' : i === currentStep ? '→' : '·'}</span>
                {step}
              </div>
            ))}
          </div>
        )}

        {/* What we check */}
        {!isLoading && (
          <div className="grid grid-cols-2 gap-3 mt-6 pt-6 border-t border-slate-100">
            {CHECKS.map(({ icon: Icon, label }) => (
              <div key={label} className="flex items-center gap-2 text-xs text-slate-500 font-medium">
                <Icon size={14} className="text-slate-400" />
                {label}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Trust row */}
      <div className="flex items-center gap-6 mt-8 flex-wrap justify-center">
        {['No signup required', 'Real checks, not templates', 'Powered by Groq AI'].map(
          (t, i) => (
            <span key={i} className="text-xs text-slate-500 font-medium flex items-center gap-1.5">
              <span className="text-blue-600">{i === 2 ? '✦' : '✓'}</span> {t}
            </span>
          )
        )}
      </div>
    </div>
  )
}
