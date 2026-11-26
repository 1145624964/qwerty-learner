import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { test } from 'node:test'

async function readJson(relativePath) {
  return JSON.parse(await readFile(new URL(`../../${relativePath}`, import.meta.url), 'utf8'))
}

test('23考研英语词汇闪过 full-book dictionary has 5566 rows, preserves homographs, and aligns with 98 chapters', async () => {
  const words = await readJson('public/dicts/shanguo_kaoyan_2023_book_order.json')
  const chapters = await readJson('src/resources/shanguo_kaoyan_2023_chapters.json')

  assert.equal(words.length, 5566)
  assert.equal(chapters.length, 98)
  assert.equal(chapters[0].start, 0)
  assert.equal(chapters.at(-1).end, words.length)
  assert.ok(chapters.every((c, idx) => idx === 0 || c.start === chapters[idx - 1].end))

  // Check section totals match book cover & structure
  const countByGroup = {}
  for (const w of words) {
    countByGroup[w.group] = (countByGroup[w.group] ?? 0) + 1
  }
  assert.deepEqual(countByGroup, {
    高频词: 826,
    中频词: 318,
    低频词: 639,
    偶考词: 1216,
    简单词: 2191,
    补充词: 376,
  })

  // Check homographs are preserved with independent IDs
  const tormentEntries = words.filter((w) => w.name === 'torment')
  assert.equal(tormentEntries.length, 2)
  assert.NotEqual?.(tormentEntries[0].id, tormentEntries[1].id)
})

test('23考研英语词汇闪过 study plan follows book order and has 98 study days + 19 review days', async () => {
  const plan = await readJson('src/resources/shanguo_kaoyan_2023_plan.json')
  assert.equal(plan.totalStudyDays, 98)
  assert.equal(plan.totalReviewDays, 19)
  assert.equal(plan.totalDays, 117)
  assert.equal(plan.totalEntries, 5566)
  assert.deepEqual(plan.groupOrder, ['高频词', '中频词', '低频词', '偶考词', '简单词', '补充词'])

  const studyTasks = plan.tasks.filter((t) => t.kind === 'study')
  const reviewTasks = plan.tasks.filter((t) => t.kind === 'review')
  assert.equal(studyTasks.length, 98)
  assert.equal(reviewTasks.length, 19)
  assert.equal(
    studyTasks.reduce((acc, t) => acc + t.newWords, 0),
    5566,
  )
  assert.ok(reviewTasks.every((t) => t.newWords === 0 && t.reviewChapterIds.length > 0))
})

test('first 68 study days (136 reading articles, all 2999 high, medium, low, and rare words) cover 100% of chapter target words and align P1-P6', async () => {
  const words = await readJson('public/dicts/shanguo_kaoyan_2023_book_order.json')
  const chapters = await readJson('src/resources/shanguo_kaoyan_2023_chapters.json')
  const articles = await readJson('src/resources/shanguo_kaoyan_2023_articles.json')

  assert.equal(articles.length, 136)

  const expectedChapterIds = chapters.slice(0, 68).map((c) => c.id)

  for (const chapId of expectedChapterIds) {
    const chap = chapters.find((c) => c.id === chapId)
    assert.ok(chap)
    const chapWords = words.slice(chap.start, chap.end)
    const chapArts = articles.filter((a) => a.chapterId === chapId)
    assert.equal(chapArts.length, 2)

    const coveredOrders = new Set()
    for (const art of chapArts) {
      assert.equal(art.paragraphs.length, 6)
      assert.equal(art.questions.length, 5)
      assert.equal(art.sentences.length, 2)
      assert.ok(art.wordCount >= 455 && art.wordCount <= 525)
      for (const g of art.glossary) {
        coveredOrders.add(g.dayOrder)
        assert.equal(g.word.toLowerCase(), chapWords[g.dayOrder - 1].name.toLowerCase())
      }
    }
    assert.equal(coveredOrders.size, chapWords.length)
  }
})
