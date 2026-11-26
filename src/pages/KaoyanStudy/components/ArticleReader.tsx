import type {
  ArticleAttemptRecord,
  ArticleGlossaryItem,
  KaoyanArticle,
  KaoyanWordEntry,
  SenseEvaluationRecord,
  SenseRating,
} from '../types'
import type React from 'react'
import { useEffect, useMemo, useState } from 'react'

type ArticleReaderProps = {
  article: KaoyanArticle
  totalDayWords: number
  dictMap: Map<string, KaoyanWordEntry>
  attempt?: ArticleAttemptRecord
  senseEvaluations: Record<string, SenseEvaluationRecord>
  onSaveAttempt: (attempt: ArticleAttemptRecord) => void
  onSaveSenseEval: (record: SenseEvaluationRecord) => void
}

const SENSE_RATING_LABELS: { value: SenseRating; label: string; colorClass: string }[] = [
  { value: 'recognized', label: '已识别本文义项', colorClass: 'bg-emerald-600 text-white border-emerald-600' },
  { value: 'guessed', label: '猜出但不确定', colorClass: 'bg-amber-500 text-white border-amber-500' },
  { value: 'unrecognized', label: '未认出', colorClass: 'bg-rose-600 text-white border-rose-600' },
  { value: 'confused', label: '容易混淆/熟词生义误判', colorClass: 'bg-purple-600 text-white border-purple-600' },
]

function extractSentenceWithSurface(paragraphText: string, surface: string): string {
  const plain = paragraphText.replace(/\*\*/g, '')
  const sentences = plain.split(/(?<=[.!?])\s+/)
  const lowerSurf = surface.toLowerCase()
  for (const s of sentences) {
    if (s.toLowerCase().includes(lowerSurf)) {
      return s.trim()
    }
  }
  return plain
}

export const ArticleReader: React.FC<ArticleReaderProps> = ({
  article,
  totalDayWords,
  dictMap,
  attempt,
  senseEvaluations,
  onSaveAttempt,
  onSaveSenseEval,
}) => {
  const [showBold, setShowBold] = useState(true)
  const [showTranslation, setShowTranslation] = useState(false)
  const [showGlossary, setShowGlossary] = useState(false)
  const [showAnalysis, setShowAnalysis] = useState(false)
  const [activeWordSurface, setActiveWordSurface] = useState<string | null>(null)
  const [answers, setAnswers] = useState<Record<number, string>>(attempt?.answers ?? {})
  const [submitted, setSubmitted] = useState<boolean>(attempt?.submitted ?? false)

  useEffect(() => {
    setAnswers(attempt?.answers ?? {})
    setSubmitted(attempt?.submitted ?? false)
    setShowAnalysis(attempt?.submitted ?? false)
    setActiveWordSurface(null)
  }, [article.id, attempt])

  // Lookup map by surface lower -> glossary or crossover item
  const surfaceMap = useMemo(() => {
    const map = new Map<
      string,
      {
        kind: 'primary' | 'crossover'
        glossary?: ArticleGlossaryItem
        word: string
        surface: string
        para: string
        meaning: string
        entry?: KaoyanWordEntry
      }
    >()

    for (const g of article.glossary) {
      const entry = dictMap.get(g.entryId)
      map.set(g.surface.toLowerCase(), {
        kind: 'primary',
        glossary: g,
        word: g.word,
        surface: g.surface,
        para: g.para,
        meaning: g.meaning,
        entry,
      })
      map.set(g.word.toLowerCase(), {
        kind: 'primary',
        glossary: g,
        word: g.word,
        surface: g.surface,
        para: g.para,
        meaning: g.meaning,
        entry,
      })
    }

    for (const c of article.crossovers ?? []) {
      if (!map.has(c.word.toLowerCase())) {
        // Find entry in dictMap by name
        let matchedEntry: KaoyanWordEntry | undefined
        dictMap.forEach((v) => {
          if (!matchedEntry && v.name.toLowerCase() === c.word.toLowerCase()) {
            matchedEntry = v
          }
        })
        map.set(c.word.toLowerCase(), {
          kind: 'crossover',
          word: c.word,
          surface: c.word,
          para: c.para,
          meaning: c.meaning,
          entry: matchedEntry,
        })
      }
    }
    return map
  }, [article, dictMap])

  const activeWordInfo = useMemo(() => {
    if (!activeWordSurface) return null
    return surfaceMap.get(activeWordSurface.toLowerCase()) ?? null
  }, [activeWordSurface, surfaceMap])

  const activeSentence = useMemo(() => {
    if (!activeWordInfo) return ''
    const firstParaMatch = activeWordInfo.para.match(/P(\d+)/)
    const pIdx = firstParaMatch ? Number(firstParaMatch[1]) - 1 : 0
    const paraTuple = article.paragraphs[pIdx] ?? article.paragraphs[0]
    return extractSentenceWithSurface(paraTuple[0], activeWordInfo.surface)
  }, [activeWordInfo, article.paragraphs])

  const handleSelectOption = (ordinal: number, optionLetter: string) => {
    const next = { ...answers, [ordinal]: optionLetter }
    setAnswers(next)
    onSaveAttempt({
      articleId: article.id,
      chapterId: article.chapterId,
      answers: next,
      submitted,
      score: attempt?.score ?? 0,
      total: article.questions.length,
      readCompleted: attempt?.readCompleted ?? false,
      updatedAt: new Date().toISOString(),
    })
  }

  const handleSubmitQuiz = () => {
    let score = 0
    for (const q of article.questions) {
      if (answers[q.ordinal] === q.answer) {
        score += 1
      }
    }
    setSubmitted(true)
    setShowAnalysis(true)
    onSaveAttempt({
      articleId: article.id,
      chapterId: article.chapterId,
      answers,
      submitted: true,
      score,
      total: article.questions.length,
      readCompleted: true,
      updatedAt: new Date().toISOString(),
    })
  }

  const handleToggleReadComplete = () => {
    const nextDone = !(attempt?.readCompleted ?? false)
    onSaveAttempt({
      articleId: article.id,
      chapterId: article.chapterId,
      answers,
      submitted,
      score: attempt?.score ?? 0,
      total: article.questions.length,
      readCompleted: nextDone,
      updatedAt: new Date().toISOString(),
    })
  }

  const renderParagraphTokens = (enText: string, pIndex: number) => {
    // Split by **word** blocks
    const parts = enText.split(/(\*\*[^*]+\*\*)/g)
    return parts.map((part, idx) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        const surface = part.slice(2, -2)
        const info = surfaceMap.get(surface.toLowerCase())
        const entryId = info?.glossary?.entryId ?? info?.entry?.id ?? surface.toLowerCase()
        const evalKey = `${article.id}::${entryId}`
        const senseEval = senseEvaluations[evalKey]
        const isSelected = activeWordSurface?.toLowerCase() === surface.toLowerCase()

        let badgeColor = ''
        if (senseEval?.rating === 'unrecognized') badgeColor = 'ring-2 ring-rose-500 bg-rose-100 dark:bg-rose-900/40'
        else if (senseEval?.rating === 'confused') badgeColor = 'ring-2 ring-purple-500 bg-purple-100 dark:bg-purple-900/40'
        else if (senseEval?.rating === 'guessed') badgeColor = 'ring-2 ring-amber-500 bg-amber-100 dark:bg-amber-900/40'
        else if (senseEval?.rating === 'recognized') badgeColor = 'bg-emerald-50 dark:bg-emerald-900/30'

        return (
          <button
            key={`${pIndex}-${idx}`}
            type="button"
            onClick={() => setActiveWordSurface(surface)}
            title="点击查看本文语境义项、搭配与原书词条详情"
            className={`mx-0.5 inline-block cursor-pointer rounded px-1 py-0.5 text-left transition-all ${
              showBold
                ? 'font-bold text-indigo-700 underline decoration-indigo-400 decoration-2 underline-offset-4 hover:bg-indigo-100 dark:text-indigo-300 dark:hover:bg-indigo-900/50'
                : 'font-normal text-gray-800 hover:bg-gray-200 dark:text-gray-100 dark:hover:bg-gray-700'
            } ${isSelected ? 'bg-indigo-200 ring-2 ring-indigo-600 dark:bg-indigo-800' : badgeColor}`}
          >
            {surface}
          </button>
        )
      }
      return <span key={`${pIndex}-${idx}`}>{part}</span>
    })
  }

  return (
    <div className="flex flex-col gap-6">
      {/* Top Meta & Controls Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 rounded-xl border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-700 dark:bg-gray-800">
        <div>
          <div className="flex flex-wrap items-center gap-2 text-xs font-semibold uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
            <span>
              {article.group}第{article.groupDay}天 · {article.wordList} · 文章{article.articleNumber}
            </span>
            <span>|</span>
            <span>计划日期：{article.scheduledDate}</span>
            <span>|</span>
            <span>正文实测：{article.wordCount} 词（6段）</span>
            <span>|</span>
            <span>
              主词表：{article.glossary.length} 词（当日合计 {totalDayWords} 词）
            </span>
          </div>
          <h2 className="mt-1 text-2xl font-bold text-gray-900 dark:text-white">{article.title}</h2>
          <p className="mt-0.5 text-sm text-gray-500 dark:text-gray-400">
            原创英语一风格词汇迁移强化阅读 · 点击文中高亮词汇即可查看「本文语境义项」并标记掌握程度
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <button
            type="button"
            onClick={() => setShowBold((b) => !b)}
            className={`rounded-lg border px-3 py-1.5 text-sm font-medium transition ${
              showBold
                ? 'border-indigo-600 bg-indigo-50 text-indigo-700 dark:border-indigo-400 dark:bg-indigo-900/30 dark:text-indigo-300'
                : 'border-gray-300 bg-white text-gray-700 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-200'
            }`}
          >
            {showBold ? '目标词加粗：开' : '无加粗复读模式'}
          </button>

          <button
            type="button"
            onClick={() => setShowTranslation((t) => !t)}
            className={`rounded-lg border px-3 py-1.5 text-sm font-medium transition ${
              showTranslation
                ? 'border-emerald-600 bg-emerald-50 text-emerald-700 dark:border-emerald-400 dark:bg-emerald-900/30 dark:text-emerald-300'
                : 'border-gray-300 bg-white text-gray-700 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-200'
            }`}
          >
            {showTranslation ? '隐藏逐段译文' : '展开逐段译文'}
          </button>

          <button
            type="button"
            onClick={() => setShowGlossary((g) => !g)}
            className={`rounded-lg border px-3 py-1.5 text-sm font-medium transition ${
              showGlossary
                ? 'border-amber-600 bg-amber-50 text-amber-700 dark:border-amber-400 dark:bg-amber-900/30 dark:text-amber-300'
                : 'border-gray-300 bg-white text-gray-700 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-200'
            }`}
          >
            {showGlossary ? '收起文后词表' : '查看本文目标词表'}
          </button>

          <button
            type="button"
            onClick={handleToggleReadComplete}
            className={`rounded-lg px-3 py-1.5 text-sm font-semibold transition ${
              attempt?.readCompleted
                ? 'bg-emerald-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200'
            }`}
          >
            {attempt?.readCompleted ? '✓ 本篇已读完' : '标记本篇已读'}
          </button>
        </div>
      </div>

      {/* Main Content + Context Word Card Side-by-Side */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        {/* Left: Paragraphs P1-P6 */}
        <div className="flex flex-col gap-4 rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800 lg:col-span-8">
          {showTranslation && (
            <div className="mb-2 rounded-lg bg-emerald-50 px-4 py-2.5 text-base font-bold text-emerald-900 dark:bg-emerald-900/30 dark:text-emerald-200">
              中文标题：{article.zhTitle}
            </div>
          )}

          {article.paragraphs.map(([enP, zhP], idx) => (
            <div
              key={idx}
              id={`para-P${idx + 1}`}
              className="border-b border-gray-100 pb-4 last:border-b-0 dark:border-gray-700"
            >
              <p className="text-base leading-8 text-gray-800 dark:text-gray-100">
                <span className="mr-2 inline-block rounded bg-gray-100 px-1.5 py-0.5 font-mono text-xs font-bold text-gray-600 dark:bg-gray-700 dark:text-gray-300">
                  [P{idx + 1}]
                </span>
                {renderParagraphTokens(enP, idx)}
              </p>
              {showTranslation && (
                <p className="mt-2 rounded-lg bg-gray-50 p-3 text-sm leading-7 text-gray-700 dark:bg-gray-900/50 dark:text-gray-300">
                  <span className="mr-1.5 font-mono text-xs font-semibold text-emerald-600 dark:text-emerald-400">
                    [译 P{idx + 1}]
                  </span>
                  {zhP}
                </p>
              )}
            </div>
          ))}
        </div>

        {/* Right: Context Word Card (First Screen focuses on context meaning) */}
        <div className="flex flex-col gap-4 lg:col-span-4">
          <div className="sticky top-4 rounded-xl border border-indigo-200 bg-white p-5 shadow-sm dark:border-indigo-800 dark:bg-gray-800">
            <div className="flex items-center justify-between border-b border-gray-100 pb-3 dark:border-gray-700">
              <h3 className="text-base font-bold text-gray-900 dark:text-white">语境词卡（先认本文义项）</h3>
              {activeWordInfo && (
                <span className="rounded bg-indigo-100 px-2 py-0.5 text-xs font-semibold text-indigo-700 dark:bg-indigo-900 dark:text-indigo-300">
                  {activeWordInfo.kind === 'primary'
                    ? `当日序号 #${activeWordInfo.glossary?.dayOrder}`
                    : '跨篇复现词'}
                </span>
              )}
            </div>

            {!activeWordInfo ? (
              <div className="py-8 text-center text-sm text-gray-500 dark:text-gray-400">
                点击左侧文章中的任意<span className="mx-1 font-bold text-indigo-600">加粗目标词</span>
                ，即可在此查看：
                <ul className="mt-3 space-y-1.5 text-left text-xs text-gray-600 dark:text-gray-300">
                  <li>• 第一屏：本文词性、本文具体义项、搭配与易混辨析</li>
                  <li>• 所在段落与完整英文原句对照</li>
                  <li>• 对该词「本文义项」的独立掌握度自评（不自动扩散到其他义项）</li>
                  <li>• 展开可查《23考研英语词汇闪过》原书完整释义、词根记忆与真题短语</li>
                </ul>
              </div>
            ) : (
              <div className="mt-3 flex flex-col gap-3 text-sm">
                <div>
                  <div className="flex items-baseline gap-2">
                    <span className="text-2xl font-extrabold text-indigo-600 dark:text-indigo-400">
                      {activeWordInfo.word}
                    </span>
                    {activeWordInfo.surface.toLowerCase() !== activeWordInfo.word.toLowerCase() && (
                      <span className="text-xs text-gray-500">（文中形式：{activeWordInfo.surface}）</span>
                    )}
                    <span className="ml-auto font-mono text-xs text-gray-500">位置：{activeWordInfo.para}</span>
                  </div>
                  {activeWordInfo.entry?.usphone && (
                    <div className="mt-1 flex items-center gap-3 font-mono text-xs text-gray-500 dark:text-gray-400">
                      <span>音标：/{activeWordInfo.entry.usphone}/</span>
                      {activeWordInfo.entry.bookPage && (
                        <span>纸书第 {activeWordInfo.entry.bookPage} 页（PDF P{activeWordInfo.entry.pdfPage}）</span>
                      )}
                    </div>
                  )}
                </div>

                {/* First Screen: Context meaning */}
                <div className="rounded-lg border border-indigo-100 bg-indigo-50/70 p-3 dark:border-indigo-900 dark:bg-indigo-950/40">
                  <div className="text-xs font-bold uppercase text-indigo-700 dark:text-indigo-300">
                    本文词性、语境义项与搭配辨析
                  </div>
                  <div className="mt-1 font-medium leading-6 text-gray-900 dark:text-gray-100">
                    {activeWordInfo.meaning}
                  </div>
                </div>

                {/* Context sentence */}
                <div className="rounded-lg bg-gray-50 p-3 dark:bg-gray-900/50">
                  <div className="text-xs font-semibold text-gray-500 dark:text-gray-400">所在原句：</div>
                  <p className="mt-1 text-xs italic leading-5 text-gray-700 dark:text-gray-300">
                    “{activeSentence}”
                  </p>
                </div>

                {/* Self-evaluation for THIS context sense */}
                <div>
                  <div className="mb-1.5 text-xs font-bold text-gray-700 dark:text-gray-300">
                    你阅读时认出「此处的义项」了吗？
                  </div>
                  <div className="grid grid-cols-2 gap-1.5">
                    {SENSE_RATING_LABELS.map((item) => {
                      const entryId =
                        activeWordInfo.glossary?.entryId ??
                        activeWordInfo.entry?.id ??
                        activeWordInfo.word.toLowerCase()
                      const evalKey = `${article.id}::${entryId}`
                      const currentRating = senseEvaluations[evalKey]?.rating
                      const active = currentRating === item.value
                      return (
                        <button
                          key={item.value}
                          type="button"
                          onClick={() =>
                            onSaveSenseEval({
                              key: evalKey,
                              articleId: article.id,
                              chapterId: article.chapterId,
                              entryId,
                              word: activeWordInfo.word,
                              surface: activeWordInfo.surface,
                              para: activeWordInfo.para,
                              meaning: activeWordInfo.meaning,
                              contextSentence: activeSentence,
                              rating: item.value,
                              updatedAt: new Date().toISOString(),
                            })
                          }
                          className={`rounded-md border px-2 py-1.5 text-xs font-medium transition ${
                            active
                              ? item.colorClass
                              : 'border-gray-200 bg-white text-gray-700 hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300'
                          }`}
                        >
                          {item.label}
                        </button>
                      )
                    })}
                  </div>
                </div>

                {/* Collapsible Full Book Entry Details */}
                {activeWordInfo.entry && (
                  <details className="mt-1 rounded-lg border border-gray-200 p-2.5 text-xs dark:border-gray-700">
                    <summary className="cursor-pointer font-semibold text-gray-700 dark:text-gray-200">
                      展开原书全义项、词根词缀与真题短语（#{activeWordInfo.entry.rowIndex + 1}）
                    </summary>
                    <div className="mt-2 space-y-2 border-t border-gray-100 pt-2 text-gray-600 dark:border-gray-700 dark:text-gray-300">
                      <div>
                        <span className="font-semibold text-gray-800 dark:text-gray-100">原书完整释义：</span>
                        {activeWordInfo.entry.trans.join('；')}
                      </div>
                      {activeWordInfo.entry.mnemonic && (
                        <div>
                          <span className="font-semibold text-indigo-600 dark:text-indigo-400">【记】</span>
                          {activeWordInfo.entry.mnemonic}
                        </div>
                      )}
                      {activeWordInfo.entry.phrases.length > 0 && (
                        <div>
                          <span className="font-semibold text-emerald-600 dark:text-emerald-400">【用·真题搭配】</span>
                          <ul className="mt-1 list-inside list-disc space-y-0.5">
                            {activeWordInfo.entry.phrases.map((p, i) => (
                              <li key={i}>{p}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      {activeWordInfo.entry.extensions.length > 0 && (
                        <div>
                          <span className="font-semibold text-amber-600 dark:text-amber-400">【扩】</span>
                          {activeWordInfo.entry.extensions.join(' ｜ ')}
                        </div>
                      )}
                    </div>
                  </details>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Collapsible Target Word Glossary & Crossovers Table */}
      {showGlossary && (
        <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white">
            本文目标词释义表（共 {article.glossary.length} 词）
          </h3>
          <p className="mt-0.5 text-xs text-gray-500">
            序号沿用当天原词表；点击任意行可定位到词卡并自评该义项掌握度。
          </p>
          <div className="mt-4 overflow-x-auto">
            <table className="w-full border-collapse text-left text-sm">
              <thead>
                <tr className="border-b border-gray-200 bg-gray-50 text-xs font-bold uppercase text-gray-600 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-300">
                  <th className="px-3 py-2">当日序号</th>
                  <th className="px-3 py-2">原词</th>
                  <th className="px-3 py-2">文中形式与段落</th>
                  <th className="px-3 py-2">本文释义、搭配与易混辨析</th>
                  <th className="px-3 py-2">本文义项自评</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                {article.glossary.map((g) => {
                  const evalKey = `${article.id}::${g.entryId}`
                  const rating = senseEvaluations[evalKey]?.rating
                  return (
                    <tr
                      key={g.dayOrder}
                      onClick={() => setActiveWordSurface(g.surface)}
                      className="cursor-pointer hover:bg-indigo-50/50 dark:hover:bg-indigo-950/30"
                    >
                      <td className="px-3 py-2 font-mono text-xs text-gray-500">{g.dayOrder}</td>
                      <td className="px-3 py-2 font-bold text-indigo-600 dark:text-indigo-400">{g.word}</td>
                      <td className="px-3 py-2 text-xs text-gray-600 dark:text-gray-300">
                        {g.surface}（{g.para}）
                      </td>
                      <td className="px-3 py-2 text-gray-800 dark:text-gray-100">{g.meaning}</td>
                      <td className="px-3 py-2 text-xs">
                        {rating ? (
                          <span className="rounded bg-gray-100 px-2 py-0.5 font-medium dark:bg-gray-700">
                            {SENSE_RATING_LABELS.find((r) => r.value === rating)?.label}
                          </span>
                        ) : (
                          <span className="text-gray-400">未评</span>
                        )}
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>

          {article.crossovers && article.crossovers.length > 0 && (
            <div className="mt-6">
              <h4 className="text-base font-bold text-gray-900 dark:text-white">当日词跨篇复现</h4>
              <div className="mt-2 overflow-x-auto">
                <table className="w-full border-collapse text-left text-sm">
                  <thead>
                    <tr className="border-b border-gray-200 bg-gray-50 text-xs font-bold uppercase text-gray-600 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-300">
                      <th className="px-3 py-2">原词</th>
                      <th className="px-3 py-2">本文位置</th>
                      <th className="px-3 py-2">本篇语境义项与搭配</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                    {article.crossovers.map((c, idx) => (
                      <tr key={idx}>
                        <td className="px-3 py-2 font-bold text-indigo-600 dark:text-indigo-400">{c.word}</td>
                        <td className="px-3 py-2 text-xs text-gray-600 dark:text-gray-300">{c.para}</td>
                        <td className="px-3 py-2 text-gray-800 dark:text-gray-100">{c.meaning}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

      {/* 5 Reading Comprehension Questions */}
      <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-gray-100 pb-4 dark:border-gray-700">
          <div>
            <h3 className="text-lg font-bold text-gray-900 dark:text-white">
              阅读理解（考研英语一风格 · 5道四选一）
            </h3>
            <p className="text-xs text-gray-500">
              先独立作答，提交后展开正确答案依据与全部三个干扰项错误原因解析。
            </p>
          </div>
          {submitted && (
            <div className="rounded-lg bg-indigo-50 px-4 py-2 text-sm font-bold text-indigo-700 dark:bg-indigo-900/40 dark:text-indigo-300">
              本次得分：{attempt?.score ?? 0} / {article.questions.length}
            </div>
          )}
        </div>

        <div className="mt-5 space-y-6">
          {article.questions.map((q) => {
            const userAns = answers[q.ordinal]
            const isCorrect = userAns === q.answer
            return (
              <div key={q.ordinal} className="rounded-lg border border-gray-100 p-4 dark:border-gray-700">
                <div className="font-semibold text-gray-900 dark:text-white">
                  {q.ordinal}. {q.stem}
                </div>
                <div className="mt-3 space-y-2">
                  {q.options.map((opt) => {
                    const letter = opt.slice(0, 1)
                    const selected = userAns === letter
                    let optStyle =
                      'border-gray-200 bg-white text-gray-800 hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200'
                    if (submitted) {
                      if (letter === q.answer) {
                        optStyle =
                          'border-emerald-500 bg-emerald-50 text-emerald-900 font-semibold dark:bg-emerald-950/50 dark:text-emerald-200'
                      } else if (selected && letter !== q.answer) {
                        optStyle =
                          'border-rose-500 bg-rose-50 text-rose-900 dark:bg-rose-950/50 dark:text-rose-200'
                      }
                    } else if (selected) {
                      optStyle =
                        'border-indigo-600 bg-indigo-50 text-indigo-900 font-semibold dark:border-indigo-400 dark:bg-indigo-950/50 dark:text-indigo-200'
                    }

                    return (
                      <button
                        key={letter}
                        type="button"
                        onClick={() => handleSelectOption(q.ordinal, letter)}
                        className={`flex w-full items-center justify-between rounded-lg border px-4 py-2.5 text-left text-sm transition ${optStyle}`}
                      >
                        <span>{opt}</span>
                        {submitted && letter === q.answer && (
                          <span className="ml-2 text-xs font-bold text-emerald-600 dark:text-emerald-400">
                            ✓ 正确答案
                          </span>
                        )}
                        {submitted && selected && !isCorrect && (
                          <span className="ml-2 text-xs font-bold text-rose-600 dark:text-rose-400">✗ 你的选择</span>
                        )}
                      </button>
                    )
                  })}
                </div>

                {showAnalysis && (
                  <div className="mt-3 rounded-lg bg-gray-50 p-3.5 text-xs leading-6 text-gray-700 dark:bg-gray-900/60 dark:text-gray-300">
                    <span className="font-bold text-indigo-600 dark:text-indigo-400">
                      【解析 · 正确答案 {q.answer}】
                    </span>{' '}
                    {q.explanation}
                  </div>
                )}
              </div>
            )
          })}
        </div>

        <div className="mt-6 flex flex-wrap items-center gap-3">
          <button
            type="button"
            onClick={handleSubmitQuiz}
            className="rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white shadow hover:bg-indigo-700"
          >
            提交答案并查看解析
          </button>
          <button
            type="button"
            onClick={() => setShowAnalysis((a) => !a)}
            className="rounded-lg border border-gray-300 px-4 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:text-gray-200"
          >
            {showAnalysis ? '收起解析与长难句' : '直接展开答案解析与长难句精读'}
          </button>
        </div>
      </div>

      {/* 2 Long & Difficult Sentences Analysis */}
      {showAnalysis && (
        <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white">长难句精读（正文实句语法与逻辑拆解）</h3>
          <div className="mt-4 space-y-4">
            {article.sentences.map((s, idx) => (
              <div key={idx} className="rounded-lg border border-indigo-100 bg-indigo-50/40 p-4 dark:border-indigo-900/60 dark:bg-indigo-950/20">
                <p className="font-serif text-sm font-semibold italic leading-6 text-gray-900 dark:text-gray-100">
                  {idx + 1}. “{s.sentence}”
                </p>
                <p className="mt-2 text-xs leading-6 text-gray-700 dark:text-gray-300">
                  <span className="font-bold text-indigo-600 dark:text-indigo-400">语法与逻辑精析：</span>
                  {s.analysis}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
