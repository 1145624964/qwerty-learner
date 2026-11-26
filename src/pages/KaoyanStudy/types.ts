export type SenseRating = 'unrecognized' | 'guessed' | 'recognized' | 'confused'

export type KaoyanWordEntry = {
  rowIndex: number
  id: string
  name: string
  rawHeadword: string
  homographIndex: string
  group: string
  wordList: string | null
  theme: string | null
  subtheme: string | null
  pdfPage: number
  bookPage: number
  sourceFile: string
  sourceLine: number
  ocrPhonetic: string
  ocrDefinition: string
  ocrPending: boolean
  mnemonic: string
  phrases: string[]
  extensions: string[]
  usphone: string
  ukphone: string
  phoneticSource: string
  trans: string[]
  notation: string
}

export type KaoyanChapter = {
  id: string
  group: string
  wordList: string | null
  groupDay: number
  name: string
  start: number
  end: number
}

export type KaoyanPlanTask = {
  id: string
  scheduledDate: string
  weekday: string
  kind: 'study' | 'review'
  learningDay: number | null
  reviewDay: number | null
  progressLabel: string
  section: string
  sectionDay: number | null
  chapterId: string | null
  reviewChapterIds: string[]
  taskLabel: string
  newWords: number
}

export type KaoyanStudyPlan = {
  id: string
  title: string
  dictionaryId: string
  targetExam: string
  timezone: string
  startDate: string
  endDate: string
  totalStudyDays: number
  totalReviewDays: number
  totalDays: number
  totalEntries: number
  groupOrder: string[]
  tasks: KaoyanPlanTask[]
}

export type ArticleGlossaryItem = {
  dayOrder: number
  word: string
  surface: string
  para: string
  meaning: string
  entryId: string
  sourceRowIndex: number
}

export type ArticleCrossoverItem = {
  word: string
  para: string
  meaning: string
}

export type ArticleQuestion = {
  ordinal: number
  stem: string
  options: string[]
  answer: string
  explanation: string
}

export type ArticleSentenceNote = {
  sentence: string
  analysis: string
}

export type KaoyanArticle = {
  id: string
  chapterId: string
  group: string
  groupDay: number
  wordList: string
  articleNumber: number
  scheduledDate: string
  title: string
  zhTitle: string
  wordCount: number
  paragraphs: [string, string][]
  glossary: ArticleGlossaryItem[]
  crossovers: ArticleCrossoverItem[]
  questions: ArticleQuestion[]
  sentences: ArticleSentenceNote[]
  sourcePath: string
}

export type SenseEvaluationRecord = {
  key: string // `${articleId}::${entryId}`
  articleId: string
  chapterId: string
  entryId: string
  word: string
  surface: string
  para: string
  meaning: string
  contextSentence: string
  rating: SenseRating
  note?: string
  updatedAt: string
}

export type ArticleAttemptRecord = {
  articleId: string
  chapterId: string
  answers: Record<number, string>
  submitted: boolean
  score: number
  total: number
  readCompleted: boolean
  updatedAt: string
}

export type TaskProgressRecord = {
  taskId: string
  chapterId: string | null
  vocabReviewed: boolean
  completed: boolean
  completedAt?: string
}

export type KaoyanPersistedState = {
  version: string
  selectedTaskId: string
  taskProgress: Record<string, TaskProgressRecord>
  articleAttempts: Record<string, ArticleAttemptRecord>
  senseEvaluations: Record<string, SenseEvaluationRecord>
  bookmarkedEntryIds: string[]
}
