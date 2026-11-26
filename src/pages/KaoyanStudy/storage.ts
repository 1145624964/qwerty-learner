import type { KaoyanPersistedState } from './types'

export const KAOYAN_STORAGE_KEY = 'kaoyanStudyState_v1'

export const DEFAULT_KAOYAN_STATE: KaoyanPersistedState = {
  version: '1.0.0',
  selectedTaskId: 'plan-study-001',
  taskProgress: {},
  articleAttempts: {},
  senseEvaluations: {},
  bookmarkedEntryIds: [],
}

export function loadKaoyanState(): KaoyanPersistedState {
  try {
    const raw = localStorage.getItem(KAOYAN_STORAGE_KEY)
    if (!raw) return DEFAULT_KAOYAN_STATE
    const parsed = JSON.parse(raw)
    if (!parsed || typeof parsed !== 'object') return DEFAULT_KAOYAN_STATE
    return {
      version: parsed.version ?? '1.0.0',
      selectedTaskId: parsed.selectedTaskId ?? 'plan-study-001',
      taskProgress: parsed.taskProgress ?? {},
      articleAttempts: parsed.articleAttempts ?? {},
      senseEvaluations: parsed.senseEvaluations ?? {},
      bookmarkedEntryIds: Array.isArray(parsed.bookmarkedEntryIds) ? parsed.bookmarkedEntryIds : [],
    }
  } catch {
    return DEFAULT_KAOYAN_STATE
  }
}

export function saveKaoyanState(state: KaoyanPersistedState): void {
  try {
    localStorage.setItem(KAOYAN_STORAGE_KEY, JSON.stringify(state))
  } catch (e) {
    console.error('Failed to save Kaoyan study state:', e)
  }
}

export function getShanghaiTodayISO(): string {
  try {
    const parts = new Intl.DateTimeFormat('en-CA', {
      timeZone: 'Asia/Shanghai',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    }).formatToParts(new Date())
    const y = parts.find((p) => p.type === 'year')?.value
    const m = parts.find((p) => p.type === 'month')?.value
    const d = parts.find((p) => p.type === 'day')?.value
    if (y && m && d) return `${y}-${m}-${d}`
  } catch {
    // fallback
  }
  return new Date().toISOString().slice(0, 10)
}
