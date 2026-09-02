import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import path from 'node:path'
import { test } from 'node:test'
import { fileURLToPath } from 'node:url'
import { createServer } from 'vite'

const projectRoot = fileURLToPath(new URL('../..', import.meta.url))

async function readJson(relativePath) {
  return JSON.parse(await readFile(new URL(`../../${relativePath}`, import.meta.url), 'utf8'))
}

function createViteTestServer() {
  return createServer({
    root: projectRoot,
    configFile: false,
    appType: 'custom',
    define: {
      REACT_APP_DEPLOY_ENV: 'undefined',
      LATEST_COMMIT_HASH: JSON.stringify('test'),
    },
    resolve: {
      alias: [
        {
          find: /^@\/utils$/,
          replacement: path.resolve(projectRoot, 'tests/integration/dictionary-utils-stub.mjs'),
        },
        { find: '@', replacement: path.resolve(projectRoot, 'src') },
      ],
    },
    server: { middlewareMode: true },
  })
}

test('daily study chapters cover every printed row exactly once and preserve order', async () => {
  const words = await readJson('public/dicts/shanguo_cet6_book_order.json')
  const chapters = await readJson('src/resources/shanguo_cet6_chapters.json')

  assert.equal(words.length, 5346)
  assert.equal(chapters.length, 92)
  assert.equal(new Set(chapters.map(({ id }) => id)).size, chapters.length)
  assert.equal(chapters[0].start, 0)
  assert.equal(chapters.at(-1).end, words.length)
  assert.ok(chapters.every((chapter, index) => index === 0 || chapter.start === chapters[index - 1].end))
  assert.ok(
    chapters.every(({ group, name }) =>
      group === '高频词' || group === '中频词' ? /^Word List \d+ · 第[12]天$/.test(name) : /^第\d+天$/.test(name),
    ),
  )
  assert.deepEqual(
    [0, 732, 733, 1737, 1738, 3135, 3136, 5345].map((index) => words[index].name),
    ['bias', 'odds', 'innovate', 'stubborn', 'skull', 'henceforth', 'beard', 'its'],
  )
  assert.ok(words.every((word) => typeof word.name === 'string' && word.name.length > 0))
  assert.ok(words.every((word) => Array.isArray(word.trans) && word.trans.length > 0))
})

test('hard-word Word Lists are split into the approved two-day workloads', async () => {
  const chapters = await readJson('src/resources/shanguo_cet6_chapters.json')
  const high = chapters.filter(({ group }) => group === '高频词')
  const medium = chapters.filter(({ group }) => group === '中频词')

  assert.deepEqual(
    high.map(({ start, end }) => end - start),
    [41, 41, 42, 41, 41, 41, 41, 41, 41, 41, 41, 40, 39, 38, 41, 40, 42, 41],
  )
  assert.deepEqual(
    medium.map(({ start, end }) => end - start),
    [42, 42, 43, 42, 42, 42, 43, 42, 43, 42, 43, 42, 42, 42, 43, 42, 39, 39, 41, 40, 42, 42, 43, 42],
  )
  assert.deepEqual(
    medium.slice(0, 4).map(({ name }) => name),
    ['Word List 1 · 第1天', 'Word List 1 · 第2天', 'Word List 2 · 第1天', 'Word List 2 · 第2天'],
  )
})

test('low-frequency and simple words use the approved daily workloads', async () => {
  const chapters = await readJson('src/resources/shanguo_cet6_chapters.json')
  const low = chapters.filter(({ group }) => group === '低频词')
  const basic = chapters.filter(({ group }) => group === '简单词')

  assert.deepEqual(
    low.map(({ start, end }) => end - start),
    [...Array(26).fill(50), 49, 49],
  )
  assert.deepEqual(
    basic.map(({ start, end }) => end - start),
    [...Array(10).fill(101), ...Array(12).fill(100)],
  )
  assert.equal(low[0].name, '第1天')
  assert.equal(low.at(-1).name, '第28天')
  assert.equal(basic[0].name, '第1天')
  assert.equal(basic.at(-1).name, '第22天')
})

test('legacy paper-order chapter state migrates without being reinterpreted as daily progress', async () => {
  const vite = await createViteTestServer()

  try {
    const { detachLegacyShanguoChapterRecord, migrateLegacyShanguoChapterIndex, migratePersistedShanguoChapterSelection } =
      await vite.ssrLoadModule('/src/utils/shanguoChapterMigration.ts')

    assert.deepEqual([0, 8, 9, 20, 21, 22].map(migrateLegacyShanguoChapterIndex), [0, 16, 18, 40, 42, 70])

    const values = new Map([
      ['currentDict', JSON.stringify('shanguo-cet6-book-order')],
      ['currentChapter', JSON.stringify(9)],
    ])
    const storage = {
      getItem: (key) => values.get(key) ?? null,
      setItem: (key, value) => values.set(key, value),
    }

    assert.equal(migratePersistedShanguoChapterSelection(storage), true)
    assert.equal(values.get('currentChapter'), JSON.stringify(18))
    values.set('currentChapter', JSON.stringify(3))
    assert.equal(migratePersistedShanguoChapterSelection(storage), false)
    assert.equal(values.get('currentChapter'), JSON.stringify(3))

    const legacyRecord = { dict: 'shanguo-cet6-book-order', chapter: 9 }
    const reviewRecord = { dict: 'shanguo-cet6-book-order', chapter: -1 }
    const otherDictionaryRecord = { dict: 'cet6', chapter: 9 }
    detachLegacyShanguoChapterRecord(legacyRecord)
    detachLegacyShanguoChapterRecord(reviewRecord)
    detachLegacyShanguoChapterRecord(otherDictionaryRecord)
    assert.equal(legacyRecord.chapter, null)
    assert.equal(reviewRecord.chapter, -1)
    assert.equal(otherDictionaryRecord.chapter, 9)
  } finally {
    await vite.close()
  }
})

test('the store migrates a persisted legacy chapter before hydrating the current selection', async () => {
  const vite = await createViteTestServer()
  const values = new Map([
    ['currentDict', JSON.stringify('shanguo-cet6-book-order')],
    ['currentChapter', JSON.stringify(9)],
  ])
  const storage = {
    getItem: (key) => values.get(key) ?? null,
    setItem: (key, value) => values.set(key, value),
    removeItem: (key) => values.delete(key),
  }
  const previousWindow = globalThis.window
  globalThis.window = {
    localStorage: storage,
    navigator: { userAgent: 'node-test' },
    document: {},
    location: { hostname: 'localhost', href: 'http://localhost/' },
    screen: {},
    console,
    matchMedia: () => ({ matches: false }),
    addEventListener: () => {},
    removeEventListener: () => {},
  }

  try {
    await vite.ssrLoadModule('/src/store/index.ts')
    assert.equal(values.get('currentChapter'), JSON.stringify(18))
  } finally {
    if (previousWindow === undefined) {
      delete globalThis.window
    } else {
      globalThis.window = previousWindow
    }
    await vite.close()
  }
})

test('the application catalog exposes the paper-order dictionary with its custom chapters', async () => {
  const vite = await createViteTestServer()

  try {
    const { dictionaryResources } = await vite.ssrLoadModule('/src/resources/dictionary.ts')
    const resource = dictionaryResources.find(({ id }) => id === 'shanguo-cet6-book-order')

    assert.ok(resource, '六级词汇闪过 should be visible in the dictionary catalog')
    assert.equal(resource.url, '/dicts/shanguo_cet6_book_order.json')
    assert.equal(resource.length, 5346)
    assert.equal(resource.description, '按纸质书正文逐行整理，保留原章节与词序，拆分为 92 个每日学习任务')
    assert.equal(resource.chapters.length, 92)
  } finally {
    await vite.close()
  }
})

test('paper-defined chapter labels stay intact outside the gallery dialog', async () => {
  const vite = await createViteTestServer()

  try {
    const { getDictionaryChapterLabel } = await vite.ssrLoadModule('/src/utils/dictionaryChapter.ts')
    assert.equal(
      getDictionaryChapterLabel({ id: 'medium-1-day-1', group: '中频词', name: 'Word List 1 · 第1天', start: 733, end: 775 }, 18),
      '中频词 · Word List 1 · 第1天',
    )
    assert.equal(getDictionaryChapterLabel({ id: '3', name: '第 3 章', start: 40, end: 60 }, 2), '第 3 章')
    assert.equal(getDictionaryChapterLabel(undefined, 4), '第 5 章')
  } finally {
    await vite.close()
  }
})
