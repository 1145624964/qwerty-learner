export const SHANGUO_CET6_DICTIONARY_ID = 'shanguo-cet6-book-order'
export const SHANGUO_CET6_CHAPTER_LAYOUT_VERSION = '2'
export const SHANGUO_CET6_CHAPTER_LAYOUT_VERSION_KEY = 'shanguoCet6ChapterLayoutVersion'

const LEGACY_LOW_FREQUENCY_CHAPTER = 21
const LEGACY_SIMPLE_WORDS_CHAPTER = 22
const FIRST_LOW_FREQUENCY_DAILY_CHAPTER = 42
const FIRST_SIMPLE_WORDS_DAILY_CHAPTER = 70

type ChapterStorage = Pick<Storage, 'getItem' | 'setItem'>
type ChapterRecordLike = { dict: string; chapter: number | null }

export function migrateLegacyShanguoChapterIndex(chapter: number) {
  if (!Number.isInteger(chapter) || chapter < 0) {
    return chapter
  }
  if (chapter < LEGACY_LOW_FREQUENCY_CHAPTER) {
    return chapter * 2
  }
  if (chapter === LEGACY_LOW_FREQUENCY_CHAPTER) {
    return FIRST_LOW_FREQUENCY_DAILY_CHAPTER
  }
  if (chapter === LEGACY_SIMPLE_WORDS_CHAPTER) {
    return FIRST_SIMPLE_WORDS_DAILY_CHAPTER
  }
  return chapter
}

export function migratePersistedShanguoChapterSelection(storage: ChapterStorage) {
  if (storage.getItem(SHANGUO_CET6_CHAPTER_LAYOUT_VERSION_KEY) === SHANGUO_CET6_CHAPTER_LAYOUT_VERSION) {
    return false
  }

  try {
    const currentDictionary = JSON.parse(storage.getItem('currentDict') ?? 'null')
    const currentChapter = JSON.parse(storage.getItem('currentChapter') ?? 'null')
    if (currentDictionary === SHANGUO_CET6_DICTIONARY_ID && Number.isInteger(currentChapter)) {
      storage.setItem('currentChapter', JSON.stringify(migrateLegacyShanguoChapterIndex(currentChapter)))
    }
  } catch {
    // Leave malformed legacy state untouched; the existing store fallback will recover it.
  }

  storage.setItem(SHANGUO_CET6_CHAPTER_LAYOUT_VERSION_KEY, SHANGUO_CET6_CHAPTER_LAYOUT_VERSION)
  return true
}

export function detachLegacyShanguoChapterRecord(record: ChapterRecordLike) {
  if (
    record.dict === SHANGUO_CET6_DICTIONARY_ID &&
    record.chapter !== null &&
    record.chapter >= 0 &&
    record.chapter <= LEGACY_SIMPLE_WORDS_CHAPTER
  ) {
    record.chapter = null
  }
}
