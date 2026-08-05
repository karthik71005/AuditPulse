import { useState, useRef } from 'react'
import { Download, FileJson, FileText, ChevronDown } from 'lucide-react'
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'

export default function DownloadButton({ report, reportRef }) {
  const [open, setOpen] = useState(false)
  const [pdfLoading, setPdfLoading] = useState(false)
  const dropdownRef = useRef(null)

  const downloadJSON = () => {
    const blob = new Blob([JSON.stringify(report, null, 2)], {
      type: 'application/json',
    })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `geo-audit-${new URL(report.url).hostname}-${Date.now()}.json`
    a.click()
    URL.revokeObjectURL(url)
    setOpen(false)
  }

  const downloadPDF = async () => {
    if (!reportRef?.current) return
    setPdfLoading(true)
    setOpen(false)
    try {
      const canvas = await html2canvas(reportRef.current, {
        backgroundColor: '#f8fafc',
        scale: 1.5,
        useCORS: true,
        logging: false,
      })
      const imgData = canvas.toDataURL('image/png')
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'px',
        format: [canvas.width / 1.5, canvas.height / 1.5],
      })
      pdf.addImage(imgData, 'PNG', 0, 0, canvas.width / 1.5, canvas.height / 1.5)
      pdf.save(`geo-audit-${new URL(report.url).hostname}-${Date.now()}.pdf`)
    } catch (e) {
      console.error('PDF generation failed', e)
    } finally {
      setPdfLoading(false)
    }
  }

  return (
    <div className="relative no-print" ref={dropdownRef}>
      <div className="flex">
        <button
          onClick={downloadPDF}
          disabled={pdfLoading}
          className="flex items-center gap-2 bg-blue-50 text-blue-700 border border-blue-200 border-r-0 px-4 py-2 rounded-l-lg text-sm font-semibold hover:bg-blue-100 transition-colors disabled:opacity-50"
        >
          <Download size={15} />
          {pdfLoading ? 'Generating…' : 'Download PDF'}
        </button>
        <button
          onClick={() => setOpen((v) => !v)}
          className="flex items-center px-2.5 py-2 bg-blue-50 text-blue-700 border border-blue-200 rounded-r-lg hover:bg-blue-100 transition-colors"
        >
          <ChevronDown size={14} />
        </button>
      </div>

      {open && (
        <div className="absolute right-0 top-full mt-1 bg-white border border-slate-200 rounded-lg shadow-xl z-50 min-w-[160px] overflow-hidden animate-fade-in text-slate-800">
          <button
            onClick={downloadPDF}
            disabled={pdfLoading}
            className="flex items-center gap-2.5 w-full px-4 py-2.5 text-sm hover:bg-slate-50 transition-colors text-left font-medium disabled:opacity-50"
          >
            <FileText size={14} className="text-slate-400" />
            Download PDF
          </button>
          <button
            onClick={downloadJSON}
            className="flex items-center gap-2.5 w-full px-4 py-2.5 text-sm hover:bg-slate-50 transition-colors text-left font-medium border-t border-slate-100"
          >
            <FileJson size={14} className="text-slate-400" />
            Download JSON
          </button>
        </div>
      )}

      {/* Close on outside click */}
      {open && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => setOpen(false)}
        />
      )}
    </div>
  )
}
