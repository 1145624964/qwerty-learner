import { ArticleReader } from './components/ArticleReader'
import { DEFAULT_KAOYAN_STATE, getShanghaiTodayISO, loadKaoyanState, saveKaoyanState } from './storage'
import type {
  ArticleAttemptRecord,
  KaoyanArticle,
  KaoyanChapter,
  KaoyanPersistedState,
  KaoyanPlanTask,
  KaoyanStudyPlan,
  KaoyanWordEntry,
  SenseEvaluationRecord,
} from './types'
import articlesData from '@/resources/shanguo_kaoyan_2023_articles.json'
import chaptersData from '@/resources/shanguo_kaoyan_2023_chapters.json'
import planData from '@/resources/shanguo_kaoyan_2023_plan.json'
import { currentChapterAtom, currentDictIdAtom } from '@/store'
import { useSetAtom } from 'jotai'
import type React from 'react'
import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'

type ActiveTab = 'today' | 'plan' | 'vocab' | 'problems' | 'data'

const KAOYAN_DICT_ID = 'kaoyan-shanguo-2023-book-order'

const plan = planData as KaoyanStudyPlan
const chapters = chaptersData as KaoyanChapter[]
const articles = articlesData as KaoyanArticle[]

export const KaoyanStudyPage: React.FC = () => {
  const navigate = useNavigate()
  const setCurrentDictId = useSetAtom(currentDictIdAtom)
  const setCurrentChapter = useSetAtom(currentChapterAtom)

  const [persisted, setPersisted] = useState<KaoyanPersistedState>(() => loadKaoyanState())
  const [dictEntries, setDictEntries] = useState<KaoyanWordEntry[]>([])
  const [isLoadingDict, setIsLoadingDict] = useState<boolean>(true)
  const [activeTab, setActiveTab] = useState<ActiveTab>('today')
  const [activeSubView, setActiveSubView] = useState<'vocab' | 'article1' | 'article2'>('vocab')
  const [planFilterSection, setPlanFilterSection] = useState<string>('全部')
  const [vocabSearch, setVocabSearch] = useState<string>('')
  const [vocabGroupFilter, setVocabGroupFilter] = useState<string>('全部')
  const [vocabPage, setVocabPage] = useState<number>(1)
  const [importMessage, setImportMessage] = useState<string>('')

  const todayISO = useMemo(() => getShanghaiTodayISO(), [])

  // Load 5566 dictionary entries
  useEffect(() => {
    let cancelled = false
    setIsLoadingDict(true)
    fetch('/dicts/shanguo_kaoyan_2023_book_order.json')
      .then((res) => res.json())
      .then((data: KaoyanWordEntry[]) => {
        if (!cancelled) {
          setDictEntries(data)
          setIsLoadingDict(false)
        }
      })
      .catch((err) => {
        console.error('Failed to load shanguo_kaoyan_2023_book_order.json:', err)
        if (!cancelled) setIsLoadingDict(false)
      })
    return () => {
      cancelled = true
    }
  }, [])

  // Save state whenever persisted changes
  useEffect(() => {
    saveKaoyanState(persisted)
  }, [persisted])

  const dictMap = useMemo(() => {
    const map = new Map<string, KaoyanWordEntry>()
    for (const e of dictEntries) {
      map.set(e.id, e)
    }
    return map
  }, [dictEntries])

  const chapterMap = useMemo(() => {
    const map = new Map<string, { chapter: KaoyanChapter; index: number }>()
    chapters.forEach((c, idx) => {
      map.set(c.id, { chapter: c, index: idx })
    })
    return map
  }, [])

  const selectedTask: KaoyanPlanTask = useMemo(() => {
    return plan.tasks.find((t) => t.id === persisted.selectedTaskId) ?? plan.tasks[0]
  }, [persisted.selectedTaskId])

  const selectedChapterInfo = useMemo(() => {
    if (!selectedTask.chapterId) return null
    return chapterMap.get(selectedTask.chapterId) ?? null
  }, [selectedTask, chapterMap])

  const dayWords: KaoyanWordEntry[] = useMemo(() => {
    if (!dictEntries.length) return []
    if (selectedTask.kind === 'study' && selectedChapterInfo) {
      const { start, end } = selectedChapterInfo.chapter
      return dictEntries.slice(start, end)
    }
    if (selectedTask.kind === 'review') {
      const list: KaoyanWordEntry[] = []
      for (const cid of selectedTask.reviewChapterIds) {
        const cInfo = chapterMap.get(cid)
        if (cInfo) {
          list.push(...dictEntries.slice(cInfo.chapter.start, cInfo.chapter.end))
        }
      }
      return list
    }
    return []
  }, [dictEntries, selectedTask, selectedChapterInfo, chapterMap])

  const dayArticles: KaoyanArticle[] = useMemo(() => {
    if (!selectedTask.chapterId) return []
    return articles
      .filter((a) => a.chapterId === selectedTask.chapterId)
      .sort((a, b) => a.articleNumber - b.articleNumber)
  }, [selectedTask])

  const handleSelectTask = (taskId: string) => {
    setPersisted((prev) => ({
      ...prev,
      selectedTaskId: taskId,
    }))
    setActiveTab('today')
    setActiveSubView('vocab')
  }

  const handlePracticeInQwerty = (chapterIndex: number) => {
    setCurrentDictId(KAOYAN_DICT_ID)
    setCurrentChapter(chapterIndex)
    navigate('/')
  }

  const handleToggleTaskComplete = (taskId: string, chapterId: string | null) => {
    setPersisted((prev) => {
      const existing = prev.taskProgress[taskId]
      const nextCompleted = !(existing?.completed ?? false)
      return {
        ...prev,
        taskProgress: {
          ...prev.taskProgress,
          [taskId]: {
            taskId,
            chapterId,
            vocabReviewed: existing?.vocabReviewed ?? true,
            completed: nextCompleted,
            completedAt: nextCompleted ? new Date().toISOString() : undefined,
          },
        },
      }
    })
  }

  const handleToggleVocabReviewed = (taskId: string, chapterId: string | null) => {
    setPersisted((prev) => {
      const existing = prev.taskProgress[taskId]
      const nextRev = !(existing?.vocabReviewed ?? false)
      return {
        ...prev,
        taskProgress: {
          ...prev.taskProgress,
          [taskId]: {
            taskId,
            chapterId,
            vocabReviewed: nextRev,
            completed: existing?.completed ?? false,
            completedAt: existing?.completedAt,
          },
        },
      }
    })
  }

  const handleToggleBookmarkWord = (entryId: string) => {
    setPersisted((prev) => {
      const exists = prev.bookmarkedEntryIds.includes(entryId)
      const next = exists
        ? prev.bookmarkedEntryIds.filter((id) => id !== entryId)
        : [...prev.bookmarkedEntryIds, entryId]
      return {
        ...prev,
        bookmarkedEntryIds: next,
      }
    })
  }

  const handleSaveAttempt = (attempt: ArticleAttemptRecord) => {
    setPersisted((prev) => ({
      ...prev,
      articleAttempts: {
        ...prev.articleAttempts,
        [attempt.articleId]: attempt,
      },
    }))
  }

  const handleSaveSenseEval = (record: SenseEvaluationRecord) => {
    setPersisted((prev) => ({
      ...prev,
      senseEvaluations: {
        ...prev.senseEvaluations,
        [record.key]: record,
      },
    }))
  }

  const handleExportProgress = () => {
    const blob = new Blob([JSON.stringify(persisted, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `kaoyan_shanguo_2023_progress_${todayISO}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  const handleImportProgress: React.ChangeEventHandler<HTMLInputElement> = (e) => {
    const file = e.target.files?.[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = () => {
      try {
        const parsed = JSON.parse(String(reader.result))
        if (parsed && typeof parsed === 'object' && parsed.taskProgress) {
          setPersisted({
            version: parsed.version ?? '1.0.0',
            selectedTaskId: parsed.selectedTaskId ?? 'plan-study-001',
            taskProgress: parsed.taskProgress ?? {},
            articleAttempts: parsed.articleAttempts ?? {},
            senseEvaluations: parsed.senseEvaluations ?? {},
            bookmarkedEntryIds: Array.isArray(parsed.bookmarkedEntryIds) ? parsed.bookmarkedEntryIds : [],
          })
          setImportMessage('✓ 学习进度恢复成功！')
        } else {
          setImportMessage('✗ 导入文件格式不正确，未找到 taskProgress 字段。')
        }
      } catch {
        setImportMessage('✗ JSON 解析失败，请检查备份文件。')
      }
    }
    reader.readAsText(file)
  }

  // Filtered vocabulary for Full Book Explorer
  const filteredVocab = useMemo(() => {
    const q = vocabSearch.trim().toLowerCase()
    return dictEntries.filter((e) => {
      if (vocabGroupFilter !== '全部' && e.group !== vocabGroupFilter) return false
      if (!q) return true
      return (
        e.name.toLowerCase().includes(q) ||
        e.trans.some((t) => t.toLowerCase().includes(q)) ||
        e.mnemonic.toLowerCase().includes(q)
      )
    })
  }, [dictEntries, vocabSearch, vocabGroupFilter])

  const PAGE_SIZE = 50
  const pagedVocab = useMemo(() => {
    const start = (vocabPage - 1) * PAGE_SIZE
    return filteredVocab.slice(start, start + PAGE_SIZE)
  }, [filteredVocab, vocabPage])

  const completedTasksCount = useMemo(() => {
    return Object.values(persisted.taskProgress).filter((p) => p.completed).length
  }, [persisted.taskProgress])

  const problemSenseRecords = useMemo(() => {
    return Object.values(persisted.senseEvaluations).filter(
      (r) => r.rating === 'unrecognized' || r.rating === 'confused' || r.rating === 'guessed',
    )
  }, [persisted.senseEvaluations])

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 dark:bg-gray-900 dark:text-gray-100">
      {/* Top Header */}
      <header className="border-b border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-800">
        <div className="container mx-auto flex flex-wrap items-center justify-between gap-4 px-6 py-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="rounded-md bg-indigo-600 px-2.5 py-0.5 text-xs font-bold text-white">
                考研全国英语一
              </span>
              <span className="rounded-md bg-amber-100 px-2.5 py-0.5 text-xs font-semibold text-amber-800 dark:bg-amber-900/40 dark:text-amber-300">
                词书：《23考研英语词汇闪过》（纸书同序 · 5566词）
              </span>
              <span className="text-xs text-gray-500 dark:text-gray-400">当前日期（Asia/Shanghai）：{todayISO}</span>
            </div>
            <h1 className="mt-1 text-2xl font-extrabold tracking-tight text-gray-900 dark:text-white">
              考研词汇与语境阅读强化系统
            </h1>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <div className="rounded-lg bg-gray-100 px-3 py-1.5 text-xs font-medium text-gray-700 dark:bg-gray-700 dark:text-gray-200">
              已确认完成：{completedTasksCount} / {plan.totalDays} 天 ｜ 语境问题词：{problemSenseRecords.length} 条
            </div>
            <button
              type="button"
              onClick={() => navigate('/')}
              className="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-200"
            >
              返回打字练习主页
            </button>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="container mx-auto flex flex-wrap gap-2 px-6 pb-3">
          {[
            { id: 'today', label: `当日学习闭环（${selectedTask.progressLabel}）` },
            { id: 'plan', label: `117天学习计划表（98学习日+19复习日）` },
            { id: 'vocab', label: `全书5566词库与词根短语检索` },
            { id: 'problems', label: `语境问题词与复习本（${problemSenseRecords.length + persisted.bookmarkedEntryIds.length}）` },
            { id: 'data', label: `词书校核、进度导出与恢复` },
          ].map((tab) => (
            <button
              key={tab.id}
              type="button"
              onClick={() => setActiveTab(tab.id as ActiveTab)}
              className={`rounded-lg px-4 py-2 text-sm font-semibold transition ${
                activeTab === tab.id
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-300'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </header>

      <main className="container mx-auto px-6 py-6">
        {isLoadingDict ? (
          <div className="flex h-64 items-center justify-center text-base font-medium text-gray-500">
            正在加载《23考研英语词汇闪过》5566条纸书同序词库...
          </div>
        ) : (
          <>
            {/* ==================== TAB 1: TODAY STUDY LOOP ==================== */}
            {activeTab === 'today' && (
              <div className="flex flex-col gap-6">
                {/* Task Banner */}
                <div className="flex flex-wrap items-center justify-between gap-4 rounded-xl border border-indigo-200 bg-white p-6 shadow-sm dark:border-indigo-900 dark:bg-gray-800">
                  <div>
                    <div className="flex flex-wrap items-center gap-2 text-xs font-bold uppercase text-indigo-600 dark:text-indigo-400">
                      <span>计划日期：{selectedTask.scheduledDate}（{selectedTask.weekday}）</span>
                      <span>•</span>
                      <span>{selectedTask.progressLabel}</span>
                      <span>•</span>
                      <span>栏目：{selectedTask.section}</span>
                      {selectedChapterInfo && (
                        <>
                          <span>•</span>
                          <span>
                            全书行区间：[{selectedChapterInfo.chapter.start}, {selectedChapterInfo.chapter.end})
                          </span>
                        </>
                      )}
                    </div>
                    <h2 className="mt-1 text-2xl font-bold text-gray-900 dark:text-white">{selectedTask.taskLabel}</h2>
                    <p className="mt-1 text-sm text-gray-600 dark:text-gray-300">
                      {selectedTask.kind === 'study'
                        ? `本日新词 ${selectedTask.newWords} 个（严格保留纸书同序、词根记忆与真题短语搭配）。配套阅读文章：${
                            dayArticles.length > 0 ? `已配套 ${dayArticles.length} 篇英语一风格强化阅读` : '待生成配套文章'
                          }。`
                        : `专门复习日：本日不学新词，重点回顾本组 ${selectedTask.reviewChapterIds.length} 个章节（共 ${dayWords.length} 词）与此前标记的语境问题词。`}
                    </p>
                  </div>

                  <div className="flex flex-wrap items-center gap-2">
                    {selectedChapterInfo && (
                      <button
                        type="button"
                        onClick={() => handlePracticeInQwerty(selectedChapterInfo.index)}
                        className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow hover:bg-indigo-700"
                      >
                        去打字背诵本章（Qwerty模式）
                      </button>
                    )}
                    <button
                      type="button"
                      onClick={() => handleToggleVocabReviewed(selectedTask.id, selectedTask.chapterId)}
                      className={`rounded-lg border px-3 py-2 text-sm font-semibold transition ${
                        persisted.taskProgress[selectedTask.id]?.vocabReviewed
                          ? 'border-emerald-600 bg-emerald-50 text-emerald-700 dark:bg-emerald-950/50 dark:text-emerald-300'
                          : 'border-gray-300 bg-white text-gray-700 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-200'
                      }`}
                    >
                      {persisted.taskProgress[selectedTask.id]?.vocabReviewed ? '✓ 当日词表已背诵' : '标记词表已背诵'}
                    </button>
                    <button
                      type="button"
                      onClick={() => handleToggleTaskComplete(selectedTask.id, selectedTask.chapterId)}
                      className={`rounded-lg px-4 py-2 text-sm font-bold transition ${
                        persisted.taskProgress[selectedTask.id]?.completed
                          ? 'bg-emerald-600 text-white'
                          : 'bg-gray-800 text-white hover:bg-gray-900 dark:bg-gray-200 dark:text-gray-900'
                      }`}
                    >
                      {persisted.taskProgress[selectedTask.id]?.completed ? '✓ 已确认完成当天学习' : '确认完成当天学习'}
                    </button>
                  </div>
                </div>

                {/* Sub-navigation: Day Vocab List vs Article 1 vs Article 2 */}
                <div className="flex flex-wrap items-center justify-between gap-4">
                  <div className="flex flex-wrap gap-2">
                    <button
                      type="button"
                      onClick={() => setActiveSubView('vocab')}
                      className={`rounded-lg px-4 py-2 text-sm font-bold transition ${
                        activeSubView === 'vocab'
                          ? 'bg-indigo-600 text-white'
                          : 'bg-white text-gray-700 shadow-sm hover:bg-gray-100 dark:bg-gray-800 dark:text-gray-200'
                      }`}
                    >
                      1. 当日原书词表（{dayWords.length} 词）
                    </button>

                    <button
                      type="button"
                      onClick={() => setActiveSubView('article1')}
                      className={`rounded-lg px-4 py-2 text-sm font-bold transition ${
                        activeSubView === 'article1'
                          ? 'bg-indigo-600 text-white'
                          : 'bg-white text-gray-700 shadow-sm hover:bg-gray-100 dark:bg-gray-800 dark:text-gray-200'
                      }`}
                    >
                      2. 英语阅读文章 1{' '}
                      {dayArticles[0]
                        ? `（${dayArticles[0].wordCount}词 · ${
                            persisted.articleAttempts[dayArticles[0].id]?.submitted
                              ? `已答 ${persisted.articleAttempts[dayArticles[0].id].score}/5`
                              : '待作答'
                          }）`
                        : '（暂未生成）'}
                    </button>

                    <button
                      type="button"
                      onClick={() => setActiveSubView('article2')}
                      className={`rounded-lg px-4 py-2 text-sm font-bold transition ${
                        activeSubView === 'article2'
                          ? 'bg-indigo-600 text-white'
                          : 'bg-white text-gray-700 shadow-sm hover:bg-gray-100 dark:bg-gray-800 dark:text-gray-200'
                      }`}
                    >
                      3. 英语阅读文章 2{' '}
                      {dayArticles[1]
                        ? `（${dayArticles[1].wordCount}词 · ${
                            persisted.articleAttempts[dayArticles[1].id]?.submitted
                              ? `已答 ${persisted.articleAttempts[dayArticles[1].id].score}/5`
                              : '待作答'
                          }）`
                        : '（暂未生成）'}
                    </button>
                  </div>

                  {/* Quick Prev/Next Day Switcher */}
                  <div className="flex items-center gap-2">
                    {(() => {
                      const curIdx = plan.tasks.findIndex((t) => t.id === selectedTask.id)
                      const prevTask = curIdx > 0 ? plan.tasks[curIdx - 1] : null
                      const nextTask = curIdx < plan.tasks.length - 1 ? plan.tasks[curIdx + 1] : null
                      return (
                        <>
                          <button
                            type="button"
                            disabled={!prevTask}
                            onClick={() => prevTask && handleSelectTask(prevTask.id)}
                            className="rounded-lg border border-gray-300 bg-white px-3 py-1.5 text-xs font-semibold text-gray-700 disabled:opacity-40 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300"
                          >
                            ← 上一天
                          </button>
                          <button
                            type="button"
                            disabled={!nextTask}
                            onClick={() => nextTask && handleSelectTask(nextTask.id)}
                            className="rounded-lg border border-gray-300 bg-white px-3 py-1.5 text-xs font-semibold text-gray-700 disabled:opacity-40 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300"
                          >
                            下一天 →
                          </button>
                        </>
                      )
                    })()}
                  </div>
                </div>

                {/* Sub-view 1: Day Vocabulary Table */}
                {activeSubView === 'vocab' && (
                  <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
                    <div className="flex flex-wrap items-center justify-between gap-4 border-b border-gray-100 pb-4 dark:border-gray-700">
                      <div>
                        <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                          {selectedTask.taskLabel} · 纸书同序词条明细
                        </h3>
                        <p className="text-xs text-gray-500">
                          保留《23考研英语词汇闪过》原书顺序、同形不同词性独立条目、词根词缀记忆法与真题短语。
                        </p>
                      </div>
                    </div>

                    <div className="mt-4 divide-y divide-gray-100 dark:divide-gray-700">
                      {dayWords.map((w, idx) => {
                        const isBookmarked = persisted.bookmarkedEntryIds.includes(w.id)
                        return (
                          <div key={w.id} className="flex flex-col gap-2 py-4 md:flex-row md:items-start md:justify-between">
                            <div className="flex-1">
                              <div className="flex flex-wrap items-baseline gap-2.5">
                                <span className="rounded bg-gray-100 px-2 py-0.5 font-mono text-xs font-bold text-gray-600 dark:bg-gray-700 dark:text-gray-300">
                                  当日 #{idx + 1}（全书 #{w.rowIndex + 1}）
                                </span>
                                <span className="text-xl font-extrabold text-indigo-600 dark:text-indigo-400">
                                  {w.name}
                                  {w.homographIndex && (
                                    <sup className="ml-0.5 text-xs font-bold text-amber-600">{w.homographIndex}</sup>
                                  )}
                                </span>
                                {w.usphone && (
                                  <span className="font-mono text-sm text-gray-500 dark:text-gray-400">
                                    /{w.usphone}/
                                  </span>
                                )}
                                <span className="text-xs text-gray-400">
                                  纸书P{w.bookPage}（PDF P{w.pdfPage}）
                                </span>
                                {w.ocrPending && (
                                  <span className="rounded bg-amber-100 px-1.5 py-0.5 text-[11px] font-medium text-amber-800 dark:bg-amber-900/40 dark:text-amber-300">
                                    含OCR待核行
                                  </span>
                                )}
                              </div>

                              <div className="mt-1.5 text-sm font-medium text-gray-900 dark:text-gray-100">
                                {w.trans.join('；')}
                              </div>

                              {w.mnemonic && (
                                <div className="mt-1.5 text-xs text-indigo-700 dark:text-indigo-300">
                                  <span className="font-bold">【记】</span>
                                  {w.mnemonic}
                                </div>
                              )}

                              {w.phrases.length > 0 && (
                                <div className="mt-1.5 flex flex-wrap gap-1.5">
                                  {w.phrases.map((phr, pIdx) => (
                                    <span
                                      key={pIdx}
                                      className="rounded-md bg-gray-100 px-2 py-0.5 text-xs text-gray-700 dark:bg-gray-700/70 dark:text-gray-300"
                                    >
                                      {phr}
                                    </span>
                                  ))}
                                </div>
                              )}

                              {w.extensions.length > 0 && (
                                <div className="mt-1 text-xs text-gray-500 dark:text-gray-400">
                                  <span className="font-semibold">【扩】</span>
                                  {w.extensions.join(' ｜ ')}
                                </div>
                              )}
                            </div>

                            <div className="flex items-center gap-2">
                              <button
                                type="button"
                                onClick={() => handleToggleBookmarkWord(w.id)}
                                className={`rounded-lg border px-3 py-1 text-xs font-semibold transition ${
                                  isBookmarked
                                    ? 'border-amber-500 bg-amber-50 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300'
                                    : 'border-gray-200 bg-white text-gray-600 hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300'
                                }`}
                              >
                                {isBookmarked ? '★ 已加入问题词本' : '☆ 标记问题词'}
                              </button>
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                )}

                {/* Sub-view 2 & 3: Article 1 or Article 2 */}
                {(activeSubView === 'article1' || activeSubView === 'article2') && (
                  <>
                    {(() => {
                      const artIdx = activeSubView === 'article1' ? 0 : 1
                      const art = dayArticles[artIdx]
                      if (!art) {
                        return (
                          <div className="rounded-xl border border-amber-200 bg-amber-50/60 p-8 text-center dark:border-amber-900 dark:bg-amber-950/30">
                            <h3 className="text-lg font-bold text-amber-900 dark:text-amber-200">
                              本章节（{selectedTask.taskLabel}）暂未导入配套阅读文章 {artIdx + 1}
                            </h3>
                            <p className="mx-auto mt-2 max-w-2xl text-sm leading-6 text-amber-800 dark:text-amber-300">
                              当前已为《23考研英语词汇闪过》生成并校核前 3 个学习日（高频词 Word List 1 第1天、第2天，Word List 2 第3天）共 6 篇英语一风格强化阅读样稿。
                              你可以先切换到学习第 1—3 天体验完整的「阅读 + 语境词卡 + 五题解析 + 长难句 + 全文译文」闭环；确认样稿风格满意后，可按相同规范批量生成后续章节文章。
                            </p>
                            <div className="mt-4 flex justify-center gap-3">
                              <button
                                type="button"
                                onClick={() => handleSelectTask('plan-study-001')}
                                className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-700"
                              >
                                跳转到学习第1天（含2篇完整配套阅读）
                              </button>
                            </div>
                          </div>
                        )
                      }
                      return (
                        <ArticleReader
                          article={art}
                          totalDayWords={dayWords.length}
                          dictMap={dictMap}
                          attempt={persisted.articleAttempts[art.id]}
                          senseEvaluations={persisted.senseEvaluations}
                          onSaveAttempt={handleSaveAttempt}
                          onSaveSenseEval={handleSaveSenseEval}
                        />
                      )
                    })()}
                  </>
                )}
              </div>
            )}

            {/* ==================== TAB 2: 117-DAY STUDY PLAN ==================== */}
            {activeTab === 'plan' && (
              <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
                <div className="flex flex-wrap items-center justify-between gap-4 border-b border-gray-100 pb-4 dark:border-gray-700">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900 dark:text-white">{plan.title}</h2>
                    <p className="mt-1 text-xs text-gray-500">
                      按原书顺序（高频词 → 中频词 → 低频词 → 偶考词 → 简单词 → 补充词）排列，共 {plan.totalStudyDays}{' '}
                      个新词学习日 + {plan.totalReviewDays} 个专门复习日 = {plan.totalDays} 天，总计 {plan.totalEntries}{' '}
                      词条。
                    </p>
                  </div>

                  <div className="flex flex-wrap gap-1.5">
                    {['全部', ...plan.groupOrder].map((sec) => (
                      <button
                        key={sec}
                        type="button"
                        onClick={() => setPlanFilterSection(sec)}
                        className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition ${
                          planFilterSection === sec
                            ? 'bg-indigo-600 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-300'
                        }`}
                      >
                        {sec}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="mt-4 overflow-x-auto">
                  <table className="w-full border-collapse text-left text-sm">
                    <thead>
                      <tr className="border-b border-gray-200 bg-gray-50 text-xs font-bold uppercase text-gray-600 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-300">
                        <th className="px-3 py-2.5">计划日期</th>
                        <th className="px-3 py-2.5">进度</th>
                        <th className="px-3 py-2.5">栏目</th>
                        <th className="px-3 py-2.5">学习或复习内容</th>
                        <th className="px-3 py-2.5">新词数</th>
                        <th className="px-3 py-2.5">配套阅读状态</th>
                        <th className="px-3 py-2.5">学习状态</th>
                        <th className="px-3 py-2.5">操作</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                      {plan.tasks
                        .filter((t) => planFilterSection === '全部' || t.section === planFilterSection)
                        .map((t) => {
                          const isToday = t.scheduledDate === todayISO
                          const prog = persisted.taskProgress[t.id]
                          const chapArts = t.chapterId ? articles.filter((a) => a.chapterId === t.chapterId) : []
                          return (
                            <tr
                              key={t.id}
                              className={`${
                                t.kind === 'review'
                                  ? 'bg-amber-50/40 dark:bg-amber-950/20'
                                  : 'hover:bg-gray-50 dark:hover:bg-gray-700/40'
                              }`}
                            >
                              <td className="px-3 py-2.5 font-mono text-xs">
                                {t.scheduledDate}（{t.weekday}）
                                {isToday && (
                                  <span className="ml-1.5 rounded bg-indigo-600 px-1.5 py-0.5 text-[10px] font-bold text-white">
                                    今日排期
                                  </span>
                                )}
                              </td>
                              <td className="px-3 py-2.5 text-xs font-semibold">{t.progressLabel}</td>
                              <td className="px-3 py-2.5 text-xs">{t.section}</td>
                              <td className="px-3 py-2.5 font-medium text-gray-900 dark:text-white">{t.taskLabel}</td>
                              <td className="px-3 py-2.5 font-mono text-xs">
                                {t.kind === 'study' ? `${t.newWords} 词` : '—'}
                              </td>
                              <td className="px-3 py-2.5 text-xs">
                                {t.kind === 'review' ? (
                                  <span className="text-amber-700 dark:text-amber-400">专门复习日</span>
                                ) : chapArts.length > 0 ? (
                                  <span className="rounded bg-emerald-100 px-2 py-0.5 font-semibold text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300">
                                    已配 {chapArts.length} 篇阅读
                                  </span>
                                ) : (
                                  <span className="text-gray-400">仅词表（阅读待扩展）</span>
                                )}
                              </td>
                              <td className="px-3 py-2.5 text-xs">
                                {prog?.completed ? (
                                  <span className="font-bold text-emerald-600 dark:text-emerald-400">✓ 已完成</span>
                                ) : prog?.vocabReviewed ? (
                                  <span className="text-indigo-600 dark:text-indigo-400">词表已背</span>
                                ) : (
                                  <span className="text-gray-400">未开始</span>
                                )}
                              </td>
                              <td className="px-3 py-2.5">
                                <button
                                  type="button"
                                  onClick={() => handleSelectTask(t.id)}
                                  className="rounded bg-indigo-50 px-2.5 py-1 text-xs font-bold text-indigo-700 hover:bg-indigo-100 dark:bg-indigo-900/50 dark:text-indigo-300"
                                >
                                  进入学习
                                </button>
                              </td>
                            </tr>
                          )
                        })}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* ==================== TAB 3: FULL 5566 VOCABULARY EXPLORER ==================== */}
            {activeTab === 'vocab' && (
              <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
                <div className="flex flex-wrap items-center justify-between gap-4 border-b border-gray-100 pb-4 dark:border-gray-700">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                      《23考研英语词汇闪过》全书纸书同序词库（5566条）
                    </h2>
                    <p className="mt-1 text-xs text-gray-500">
                      高频 826 + 中频 318 + 低频 639 + 偶考 1216（含18对同形异音词条）+ 简单 2191（含21对同形异音词条）+ 补充 376（含1对同形词条）。
                    </p>
                  </div>

                  <div className="flex flex-wrap items-center gap-2">
                    <input
                      type="text"
                      value={vocabSearch}
                      onChange={(e) => {
                        setVocabSearch(e.target.value)
                        setVocabPage(1)
                      }}
                      placeholder="搜索英文拼写、中文释义或词根..."
                      className="w-64 rounded-lg border border-gray-300 px-3 py-1.5 text-sm focus:border-indigo-500 focus:outline-none dark:border-gray-600 dark:bg-gray-700"
                    />
                    <select
                      value={vocabGroupFilter}
                      onChange={(e) => {
                        setVocabGroupFilter(e.target.value)
                        setVocabPage(1)
                      }}
                      className="rounded-lg border border-gray-300 px-3 py-1.5 text-sm dark:border-gray-600 dark:bg-gray-700"
                    >
                      {['全部', '高频词', '中频词', '低频词', '偶考词', '简单词', '补充词'].map((g) => (
                        <option key={g} value={g}>
                          {g}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="mt-3 flex items-center justify-between text-xs text-gray-500">
                  <span>共检索到 {filteredVocab.length} 条记录（保留同形不同词性/读音独立行）</span>
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      disabled={vocabPage <= 1}
                      onClick={() => setVocabPage((p) => Math.max(1, p - 1))}
                      className="rounded border px-2 py-1 disabled:opacity-40"
                    >
                      上一页
                    </button>
                    <span>
                      第 {vocabPage} / {Math.max(1, Math.ceil(filteredVocab.length / PAGE_SIZE))} 页
                    </span>
                    <button
                      type="button"
                      disabled={vocabPage >= Math.ceil(filteredVocab.length / PAGE_SIZE)}
                      onClick={() => setVocabPage((p) => p + 1)}
                      className="rounded border px-2 py-1 disabled:opacity-40"
                    >
                      下一页
                    </button>
                  </div>
                </div>

                <div className="mt-3 divide-y divide-gray-100 dark:divide-gray-700">
                  {pagedVocab.map((w) => {
                    const isBookmarked = persisted.bookmarkedEntryIds.includes(w.id)
                    return (
                      <div key={w.id} className="flex flex-col gap-1.5 py-3 md:flex-row md:items-center md:justify-between">
                        <div>
                          <div className="flex flex-wrap items-baseline gap-2">
                            <span className="font-mono text-xs text-gray-400">#{w.rowIndex + 1}</span>
                            <span className="text-base font-bold text-indigo-600 dark:text-indigo-400">
                              {w.name}
                              {w.homographIndex && <sup className="ml-0.5 text-xs text-amber-600">{w.homographIndex}</sup>}
                            </span>
                            {w.usphone && <span className="font-mono text-xs text-gray-500">/{w.usphone}/</span>}
                            <span className="rounded bg-gray-100 px-1.5 py-0.5 text-[11px] text-gray-600 dark:bg-gray-700 dark:text-gray-300">
                              {w.group} {w.wordList ?? (w.subtheme ? `· ${w.theme}/${w.subtheme}` : '')}
                            </span>
                            <span className="text-[11px] text-gray-400">
                              书内页P{w.bookPage}（PDF P{w.pdfPage}）
                            </span>
                          </div>
                          <div className="mt-0.5 text-sm text-gray-800 dark:text-gray-200">{w.trans.join('；')}</div>
                          {w.mnemonic && <div className="text-xs text-indigo-600 dark:text-indigo-400">【记】{w.mnemonic}</div>}
                        </div>
                        <button
                          type="button"
                          onClick={() => handleToggleBookmarkWord(w.id)}
                          className={`self-start rounded border px-2.5 py-1 text-xs font-medium md:self-center ${
                            isBookmarked
                              ? 'border-amber-500 bg-amber-50 text-amber-700'
                              : 'border-gray-200 text-gray-600 hover:bg-gray-50 dark:border-gray-700 dark:text-gray-300'
                          }`}
                        >
                          {isBookmarked ? '★ 已收藏' : '☆ 收藏'}
                        </button>
                      </div>
                    )
                  })}
                </div>
              </div>
            )}

            {/* ==================== TAB 4: PROBLEM WORDS & CONTEXT REVIEW ==================== */}
            {activeTab === 'problems' && (
              <div className="flex flex-col gap-6">
                <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
                  <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                    语境义项问题词本（按文章具体义项与原句回查）
                  </h2>
                  <p className="mt-1 text-xs text-gray-500">
                    记录你在阅读中标记为「未认出」「容易混淆/熟词生义误判」或「猜出但不确定」的具体语境义项。认识一个义项不会自动覆盖该词的其他义项。
                  </p>

                  {problemSenseRecords.length === 0 ? (
                    <div className="py-10 text-center text-sm text-gray-400">
                      暂无语境问题词记录。在阅读文章时点击加粗目标词并在右侧词卡自评为「未认出 / 易混淆 / 猜出但不确定」，即可自动归集到此处。
                    </div>
                  ) : (
                    <div className="mt-4 divide-y divide-gray-100 dark:divide-gray-700">
                      {problemSenseRecords.map((rec) => {
                        const art = articles.find((a) => a.id === rec.articleId)
                        return (
                          <div key={rec.key} className="py-4">
                            <div className="flex flex-wrap items-center gap-2">
                              <span className="text-lg font-extrabold text-indigo-600 dark:text-indigo-400">
                                {rec.word}
                              </span>
                              <span className="rounded bg-rose-100 px-2 py-0.5 text-xs font-bold text-rose-800 dark:bg-rose-900/40 dark:text-rose-300">
                                {rec.rating === 'unrecognized'
                                  ? '未认出'
                                  : rec.rating === 'confused'
                                  ? '容易混淆/熟词生义'
                                  : '猜出但不确定'}
                              </span>
                              <span className="text-xs text-gray-500">
                                来源：{art ? `${art.group}第${art.groupDay}天 · 文章${art.articleNumber} (${rec.para})` : rec.articleId}
                              </span>
                            </div>
                            <div className="mt-1.5 text-sm font-semibold text-gray-900 dark:text-gray-100">
                              本文语境义项：{rec.meaning}
                            </div>
                            <div className="mt-1 rounded bg-gray-50 p-2.5 text-xs italic text-gray-600 dark:bg-gray-900/50 dark:text-gray-300">
                              原句：“{rec.contextSentence}”
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  )}
                </div>

                <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                    词表收藏夹（共 {persisted.bookmarkedEntryIds.length} 词）
                  </h3>
                  {persisted.bookmarkedEntryIds.length === 0 ? (
                    <div className="py-6 text-center text-sm text-gray-400">暂无手动收藏的词表词条。</div>
                  ) : (
                    <div className="mt-3 divide-y divide-gray-100 dark:divide-gray-700">
                      {persisted.bookmarkedEntryIds.map((id) => {
                        const w = dictMap.get(id)
                        if (!w) return null
                        return (
                          <div key={id} className="flex items-center justify-between py-3">
                            <div>
                              <span className="font-bold text-indigo-600 dark:text-indigo-400">{w.name}</span>
                              <span className="ml-2 font-mono text-xs text-gray-500">/{w.usphone}/</span>
                              <span className="ml-3 text-sm text-gray-800 dark:text-gray-200">{w.trans.join('；')}</span>
                            </div>
                            <button
                              type="button"
                              onClick={() => handleToggleBookmarkWord(id)}
                              className="text-xs text-rose-600 hover:underline"
                            >
                              移除
                            </button>
                          </div>
                        )
                      })}
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* ==================== TAB 5: DATA VERIFICATION & BACKUP ==================== */}
            {activeTab === 'data' && (
              <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
                <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
                  <h2 className="text-lg font-bold text-gray-900 dark:text-white">
                    《23考研英语词汇闪过》OCR清洗与交叉校核报告
                  </h2>
                  <ul className="mt-4 space-y-2.5 text-sm leading-6 text-gray-700 dark:text-gray-300">
                    <li>
                      • <strong>纸书来源</strong>：《23考研英语词汇闪过》（张国静主编，514页扫描PDF全文OCR，97份分册Markdown）。
                    </li>
                    <li>
                      • <strong>全书词条总数</strong>：<strong>5566 条原书行</strong>（覆盖前言标称的 5526 个主词，外加 40 对同形异音/不同词性独立条目，如 <code>torment¹/²</code>、<code>refund¹/²</code>、<code>inland¹/²</code>、<code>digest¹/²</code>、<code>record¹/²</code>、<code>project¹/²</code>、<code>use¹/²</code> 等，严格遵循“同形词不按拼写去重”约束）。
                    </li>
                    <li>
                      • <strong>各栏目精确核验</strong>：
                      <ul className="ml-5 mt-1 list-disc text-xs space-y-1">
                        <li>高频词（Word List 1—10）：826 词（与封面标称 826 完全一致，0误差）</li>
                        <li>中频词（Word List 11—14）：318 词（与封面标称 318 完全一致，0误差）</li>
                        <li>低频词（Word List 15—22）：639 词（与封面标称 639 完全一致，0误差）</li>
                        <li>偶考词（7大主题场景）：1216 条词条（1198主词 + 18对同形分列词条）</li>
                        <li>简单词（7大主题场景）：2191 条词条（2170主词 + 21对同形分列词条）</li>
                        <li>补充词（真题非大纲词）：376 条词条（375主词 + 1对同形分列词条 <code>quadruple¹/²</code>）</li>
                      </ul>
                    </li>
                    <li>
                      • <strong>OCR 瑕疵定点修复与音标校核</strong>：修复了原稿中 17 处因上标 <code>²</code> 导致未加粗的词条、2 处漏竖线词条（<code>put[put]</code>、<code>fail[fen]</code>）、以及 9 处将上标 <code>¹/²</code> 误识为字母的词头（如 <code>delegater → delegate²</code>、<code>outsider → outside¹</code>、<code>rebel? → rebel²</code>、<code>recta ngle → rectangle</code> 等）；97.5% 的词条已与既有校验词库对齐标准美式/英式音标，同时保留原始 OCR 页码与待核标记。
                    </li>
                    <li>
                      • <strong>与候选词表 <code>kaoyanshanguo2025.json</code> 对照说明</strong>：经交叉核验，<code>kaoyanshanguo2025.json</code>（2257行，无音标）为25版乱序精简候选表，其中有 15 处末尾字母 <code>y</code> 脱落的拼写残缺（如 <code>liabilit</code>、<code>ordinar</code>）且缺漏部分高频词；因此系统独立采用本次完整清洗校核的 5566 条《23考研英语词汇闪过》作为正式词书版本。
                    </li>
                  </ul>
                </div>

                <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
                  <h2 className="text-lg font-bold text-gray-900 dark:text-white">学习进度备份、导出与恢复</h2>
                  <p className="mt-1 text-xs text-gray-500">
                    你的每日完成状态、阅读答题记录、语境义项自评和收藏词均独立保存在浏览器本地存储中，可随时导出 JSON 备份或在干净环境中恢复。
                  </p>

                  <div className="mt-5 flex flex-col gap-4">
                    <div className="rounded-lg bg-gray-50 p-4 text-xs leading-6 text-gray-700 dark:bg-gray-900/50 dark:text-gray-300">
                      <div>当前词书版本：<code>kaoyan-shanguo-2023-book-order</code>（5566行，98章）</div>
                      <div>当前计划版本：<code>kaoyan-shanguo-2023-plan-v1</code>（117天）</div>
                      <div>已完成任务数：{completedTasksCount} 天</div>
                      <div>已提交阅读答卷：{Object.values(persisted.articleAttempts).filter((a) => a.submitted).length} 篇</div>
                      <div>已记录语境义项自评：{Object.keys(persisted.senseEvaluations).length} 条</div>
                    </div>

                    <div className="flex flex-wrap items-center gap-3">
                      <button
                        type="button"
                        onClick={handleExportProgress}
                        className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow hover:bg-indigo-700"
                      >
                        导出学习进度 (JSON)
                      </button>

                      <label className="cursor-pointer rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-200">
                        从 JSON 备份恢复进度
                        <input type="file" accept=".json" onChange={handleImportProgress} className="hidden" />
                      </label>

                      <button
                        type="button"
                        onClick={() => {
                          if (window.confirm('确定要清空所有本地学习进度记录吗？此操作不可撤销。')) {
                            setPersisted(DEFAULT_KAOYAN_STATE)
                            setImportMessage('已重置为初始干净状态。')
                          }
                        }}
                        className="rounded-lg border border-rose-300 px-3 py-2 text-xs font-semibold text-rose-600 hover:bg-rose-50"
                      >
                        重置本地进度
                      </button>
                    </div>

                    {importMessage && (
                      <div className="rounded-lg bg-indigo-50 p-3 text-xs font-semibold text-indigo-800 dark:bg-indigo-900/40 dark:text-indigo-200">
                        {importMessage}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  )
}

export default KaoyanStudyPage
