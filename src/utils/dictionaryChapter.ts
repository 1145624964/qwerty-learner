import type { DictionaryChapter } from '@/typings'

export function getDictionaryChapterLabel(chapter: DictionaryChapter | undefined, index: number) {
  if (!chapter) {
    return `第 ${index + 1} 章`
  }
  return chapter.group ? `${chapter.group} · ${chapter.name}` : chapter.name
}
