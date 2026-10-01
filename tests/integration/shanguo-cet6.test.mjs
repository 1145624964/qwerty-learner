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
      group === '高频词' || group === '中频词' ? /^Word List \d+ · 第\d+天$/.test(name) : /^第\d+天$/.test(name),
    ),
  )
  assert.deepEqual(
    [0, 732, 733, 1737, 1738, 3135, 3136, 5345].map((index) => words[index].name),
    ['bias', 'odds', 'innovate', 'stubborn', 'skull', 'henceforth', 'beard', 'its'],
  )
  assert.ok(words.every((word) => typeof word.name === 'string' && word.name.length > 0))
  assert.ok(words.every((word) => Array.isArray(word.trans) && word.trans.length > 0))
})

test('paper-specific meanings override broader dictionary definitions', async () => {
  const words = await readJson('public/dicts/shanguo_cet6_book_order.json')
  const chapters = await readJson('src/resources/shanguo_cet6_chapters.json')
  const firstMediumDay = chapters.find(({ id }) => id === 'medium-1-day-1')

  assert.ok(firstMediumDay)
  const dailyWords = words.slice(firstMediumDay.start, firstMediumDay.end)
  const relish = dailyWords.find(({ name }) => name === 'relish')

  assert.ok(relish, 'relish should stay in 中频词 Word List 1 · 第1天')
  assert.deepEqual(relish.trans, ['vt. 期待；享受 n. [U] 享受；乐趣'])
})

test('all high-frequency entries publish the canonical paper definitions', async () => {
  const words = await readJson('public/dicts/shanguo_cet6_book_order.json')
  const definitions = await readJson('scripts/shanguo_high_book_translations.json')
  const highWords = words.slice(0, 733)

  assert.equal(definitions.length, 733)
  assert.deepEqual(
    definitions.map(({ name }) => name),
    highWords.map(({ name }) => name),
  )
  assert.ok(definitions.every(({ trans }) => typeof trans === 'string' && trans.length > 0))
  assert.ok(definitions.every(({ bookPage }) => Number.isInteger(bookPage) && bookPage >= 1 && bookPage <= 155))
  assert.ok(definitions.every(({ trans }) => /(?:^|\s)(?:n|v|vt|vi|a|ad|prep|conj|pron|num)\./.test(trans)))
  assert.ok(definitions.every(({ trans }) => !/[|+]|\.{2,}|[\u4e00-\u9fff][lJ]|[lJ][\u4e00-\u9fff]/.test(trans)))
  assert.deepEqual(
    highWords.map(({ trans }) => trans),
    definitions.map(({ trans }) => [trans]),
  )
  const definitionsByName = Object.fromEntries(definitions.map(({ name, trans }) => [name, trans]))
  assert.deepEqual(
    {
      bias: definitionsByName.bias,
      abuse: definitionsByName.abuse,
      agent: definitionsByName.agent,
      statistic: definitionsByName.statistic,
      fake: definitionsByName.fake,
      dozen: definitionsByName.dozen,
      odds: definitionsByName.odds,
    },
    {
      bias: 'n. [常用 sing., U] 偏见；[常用 sing.] 偏爱',
      abuse: 'n. [U, sing.] 滥用；[U] 辱骂；虐待 vt. 滥用；虐待',
      agent: 'n. [C] 代理人，经纪人；原动力；间谍',
      statistic: 'n. [pl.] 统计数字；[C] （一项）统计数据；[U] [-s] 统计学',
      fake: 'a. 假的；伪造的 vt. 伪造；佯装 n. [C] 赝品',
      dozen: '（abbr. doz.） n. [C] 一打，十二个；十多个；[pl.] 很多',
      odds: 'n. [pl.] 概率；逆境；不利条件',
    },
  )
})

test('all medium-frequency entries publish the canonical paper definitions', async () => {
  const words = await readJson('public/dicts/shanguo_cet6_book_order.json')
  const definitions = await readJson('scripts/shanguo_medium_book_translations.json')
  const mediumWords = words.slice(733, 1738)

  assert.equal(definitions.length, 1005)
  assert.deepEqual(
    definitions.map(({ name }) => name),
    mediumWords.map(({ name }) => name),
  )
  assert.ok(definitions.every(({ trans }) => typeof trans === 'string' && trans.length > 0))
  assert.ok(definitions.every(({ bookPage }) => Number.isInteger(bookPage) && bookPage >= 156 && bookPage <= 332))
  assert.ok(definitions.every(({ trans }) => /(?:^|\s)(?:n|v|vt|vi|a|ad|prep)\./.test(trans)))
  assert.ok(definitions.every(({ trans }) => !/[|△·]|\.{2,}|[\u4e00-\u9fff]l|l[\u4e00-\u9fff]/.test(trans)))
  assert.deepEqual(
    mediumWords.map(({ trans }) => trans),
    definitions.map(({ trans }) => [trans]),
  )
  assert.equal(definitions[0].trans, 'v. 创新')
  assert.equal(definitions[6].trans, 'vt. 期待；享受 n. [U] 享受；乐趣')
  assert.equal(definitions.at(-1).trans, 'a. 固执的；倔强的；难以去除（或对付）的')
})

test('all low-frequency entries publish the canonical paper definitions', async () => {
  const words = await readJson('public/dicts/shanguo_cet6_book_order.json')
  const definitions = await readJson('scripts/shanguo_low_book_translations.json')
  const lowWords = words.slice(1738, 3136)

  assert.equal(definitions.length, 1398)
  assert.deepEqual(
    definitions.map(({ name }) => name),
    lowWords.map(({ name }) => name),
  )
  assert.ok(definitions.every(({ trans }) => typeof trans === 'string' && trans.length > 0))
  assert.ok(definitions.every(({ bookPage }) => Number.isInteger(bookPage) && bookPage >= 333 && bookPage <= 379))
  assert.ok(definitions.every(({ bookPage }, index) => index === 0 || definitions[index - 1].bookPage <= bookPage))
  assert.deepEqual(
    Array.from({ length: 47 }, (_, index) => {
      const bookPage = 333 + index
      const pageWords = definitions.filter((definition) => definition.bookPage === bookPage)
      return [bookPage, pageWords.length, pageWords[0]?.name, pageWords.at(-1)?.name]
    }),
    [
      [333, 20, 'skull', 'thumb'],
      [334, 29, 'wrist', 'waive'],
      [335, 32, 'harass', 'knot'],
      [336, 32, 'tow', 'glare'],
      [337, 32, 'steer', 'disregard'],
      [338, 32, 'emulate', 'sprawl'],
      [339, 32, 'summon', 'dispatch'],
      [340, 32, 'disperse', 'glide'],
      [341, 30, 'limp', 'jolly'],
      [342, 32, 'lyric', 'indignant'],
      [343, 30, 'outrage', 'stern'],
      [344, 30, 'solemn', 'slender'],
      [345, 29, 'wrinkle', 'murmur'],
      [346, 30, 'mutter', 'spade'],
      [347, 32, 'bolt', 'bead'],
      [348, 30, 'portfolio', 'lime'],
      [349, 28, 'pasta', 'linen'],
      [350, 28, 'pearl', 'lodge'],
      [351, 32, 'aisle', 'strait'],
      [352, 27, 'terrain', 'federation'],
      [353, 32, 'cabinet', 'dividend'],
      [354, 30, 'allowance', 'casino'],
      [355, 30, 'comic', 'indict'],
      [356, 32, 'plaintiff', 'loot'],
      [357, 30, 'assassinate', 'herb'],
      [358, 24, 'bandage', 'aluminum'],
      [359, 30, 'mercury', 'moist'],
      [360, 28, 'humid', 'clockwise'],
      [361, 30, 'inland', 'hawk'],
      [362, 32, 'parrot', 'ripe'],
      [363, 27, 'scent', 'singular'],
      [364, 30, 'decimal', 'hockey'],
      [365, 29, 'ballet', 'analogy'],
      [366, 29, 'porcelain', 'parallel'],
      [367, 32, 'authentic', 'watertight'],
      [368, 32, 'lunar', 'hysterical'],
      [369, 32, 'impromptu', 'static'],
      [370, 30, 'tertiary', 'soar'],
      [371, 32, 'stain', 'stagnate'],
      [372, 30, 'stipulate', 'passer-by'],
      [373, 32, 'exponent', 'slogan'],
      [374, 32, 'transcript', 'paradox'],
      [375, 32, 'parade', 'cavity'],
      [376, 32, 'clearance', 'hurdle'],
      [377, 31, 'impetus', 'rust'],
      [378, 30, 'saddle', 'atop'],
      [379, 9, 'anew', 'henceforth'],
    ],
  )
  assert.ok(definitions.every(({ trans }) => /(?:^|\s)(?:n|v|vt|vi|a|ad|prep)\./.test(trans)))
  assert.ok(
    definitions.every(
      ({ trans }) => !/[|�]|\.{2,}|[\u4e00-\u9fff][lI]|[lI][\u4e00-\u9fff]|\[sing, , U\]|烟肉|内江|器血|跟跎|骤子|坪击/.test(trans),
    ),
  )
  assert.deepEqual(
    lowWords.map(({ trans }) => trans),
    definitions.map(({ trans }) => [trans]),
  )
  assert.equal(definitions[0].trans, 'n. [C] 头骨，颅骨')
  assert.equal(definitions[3].trans, 'n. [C] 颏，下巴')
  assert.equal(definitions[457].trans, 'n. [C] 卷轴 vi. 踉跄；感到震惊')
  assert.deepEqual(
    definitions.slice(783, 785).map(({ trans }) => trans),
    ['n. [C, U] 合金', 'vt. 把……铸成合金'],
  )
  assert.deepEqual(
    definitions.slice(835, 837).map(({ trans }) => trans),
    ['ad. 在内地；向内陆', 'a. 内地的；内陆的'],
  )
  assert.equal(definitions[1352].trans, 'n. [C] 原型；雏形；典型')
  assert.equal(definitions.at(-1).trans, 'ad. 此后；从此以后')
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
    high.map(({ name }) => name),
    [
      'Word List 1 · 第1天',
      'Word List 1 · 第2天',
      'Word List 2 · 第3天',
      'Word List 2 · 第4天',
      'Word List 3 · 第5天',
      'Word List 3 · 第6天',
      'Word List 4 · 第7天',
      'Word List 4 · 第8天',
      'Word List 5 · 第9天',
      'Word List 5 · 第10天',
      'Word List 6 · 第11天',
      'Word List 6 · 第12天',
      'Word List 7 · 第13天',
      'Word List 7 · 第14天',
      'Word List 8 · 第15天',
      'Word List 8 · 第16天',
      'Word List 9 · 第17天',
      'Word List 9 · 第18天',
    ],
  )
  assert.deepEqual(
    medium.map(({ name }) => name),
    [
      'Word List 1 · 第1天',
      'Word List 1 · 第2天',
      'Word List 2 · 第3天',
      'Word List 2 · 第4天',
      'Word List 3 · 第5天',
      'Word List 3 · 第6天',
      'Word List 4 · 第7天',
      'Word List 4 · 第8天',
      'Word List 5 · 第9天',
      'Word List 5 · 第10天',
      'Word List 6 · 第11天',
      'Word List 6 · 第12天',
      'Word List 7 · 第13天',
      'Word List 7 · 第14天',
      'Word List 8 · 第15天',
      'Word List 8 · 第16天',
      'Word List 9 · 第17天',
      'Word List 9 · 第18天',
      'Word List 10 · 第19天',
      'Word List 10 · 第20天',
      'Word List 11 · 第21天',
      'Word List 11 · 第22天',
      'Word List 12 · 第23天',
      'Word List 12 · 第24天',
    ],
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
    assert.equal(
      getDictionaryChapterLabel({ id: 'medium-2-day-1', group: '中频词', name: 'Word List 2 · 第3天', start: 817, end: 860 }, 20),
      '中频词 · Word List 2 · 第3天',
    )
    assert.equal(getDictionaryChapterLabel({ id: '3', name: '第 3 章', start: 40, end: 60 }, 2), '第 3 章')
    assert.equal(getDictionaryChapterLabel(undefined, 4), '第 5 章')
  } finally {
    await vite.close()
  }
})
