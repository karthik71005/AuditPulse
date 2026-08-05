// Cache key constants
const CACHE_KEY_REPORT = 'geo_auditor_report'
const CACHE_KEY_URL = 'geo_auditor_url'

export function saveReport(url, report) {
  try {
    localStorage.setItem(CACHE_KEY_URL, url)
    localStorage.setItem(CACHE_KEY_REPORT, JSON.stringify(report))
  } catch (e) {
    console.warn('Failed to save report to localStorage', e)
  }
}

export function loadReport() {
  try {
    const url = localStorage.getItem(CACHE_KEY_URL)
    const raw = localStorage.getItem(CACHE_KEY_REPORT)
    if (!url || !raw) return null
    return { url, report: JSON.parse(raw) }
  } catch (e) {
    console.warn('Failed to load report from localStorage', e)
    return null
  }
}

export function clearReport() {
  localStorage.removeItem(CACHE_KEY_URL)
  localStorage.removeItem(CACHE_KEY_REPORT)
}
