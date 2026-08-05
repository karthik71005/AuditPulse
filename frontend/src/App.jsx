import { useState, useEffect } from 'react'
import { QueryClient, QueryClientProvider, useMutation } from '@tanstack/react-query'
import LandingView from './components/LandingView'
import ReportView from './components/ReportView'
import { runAudit } from './lib/api'
import { saveReport, loadReport, clearReport } from './lib/cache'
import './index.css'

const queryClient = new QueryClient()

function GeoAuditor() {
  const [report, setReport] = useState(null)
  const [error, setError] = useState(null)

  // Restore last report from localStorage on mount
  useEffect(() => {
    const cached = loadReport()
    if (cached?.report) {
      setReport(cached.report)
    }
  }, [])

  const mutation = useMutation({
    mutationFn: runAudit,
    onSuccess: (data, url) => {
      setReport(data)
      setError(null)
      saveReport(url, data)
    },
    onError: (err) => {
      setError(err.message)
    },
  })

  const handleAudit = (url) => {
    setError(null)
    mutation.mutate(url)
  }

  const handleReset = () => {
    setReport(null)
    setError(null)
    mutation.reset()
    clearReport()
  }

  if (report && !mutation.isPending) {
    return <ReportView report={report} onReset={handleReset} />
  }

  return (
    <div>
      <LandingView onAudit={handleAudit} isLoading={mutation.isPending} />
      {error && (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 bg-red-50 border border-red-200 text-red-700 text-sm px-5 py-3 rounded-xl max-w-lg text-center animate-fade-in z-50 shadow-xl">
          <strong>Audit failed:</strong> {error}
        </div>
      )}
    </div>
  )
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <GeoAuditor />
    </QueryClientProvider>
  )
}
