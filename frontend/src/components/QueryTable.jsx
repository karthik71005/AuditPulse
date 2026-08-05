import { CheckCircle, XCircle } from 'lucide-react'

export default function QueryTable({ queries }) {
  return (
    <div className="flex flex-col gap-2.5">
      {queries.map((item, i) => (
        <div
          key={i}
          className="flex items-center gap-3 bg-white border border-slate-200 rounded-lg px-4 py-3 shadow-sm hover:border-slate-300 transition-colors"
        >
          {item.cited ? (
            <CheckCircle size={18} className="text-emerald-600 flex-shrink-0" />
          ) : (
            <XCircle size={18} className="text-red-500 flex-shrink-0" />
          )}
          <span className="text-sm flex-1 text-slate-800 font-medium">"{item.query}"</span>
          <span
            className={`text-[10px] font-bold tracking-wide uppercase px-2.5 py-1 rounded-full border flex-shrink-0 ${
              item.cited
                ? 'text-emerald-700 bg-emerald-50 border-emerald-200'
                : 'text-red-700 bg-red-50 border-red-200'
            }`}
          >
            {item.cited ? 'CITED' : 'NOT FOUND'}
          </span>
        </div>
      ))}
    </div>
  )
}
