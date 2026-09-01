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

test('the published dictionary preserves every printed row and all 23 contiguous sections', async () => {
  const words = await readJson('public/dicts/shanguo_cet6_book_order.json')
  const chapters = await readJson('src/resources/shanguo_cet6_chapters.json')

  assert.equal(words.length, 5346)
  assert.equal(chapters.length, 23)
  assert.deepEqual(
    chapters.map(({ group, start, end }) => [group, start, end]),
    [
      ['高频词', 0, 82],
      ['高频词', 82, 165],
      ['高频词', 165, 247],
      ['高频词', 247, 329],
      ['高频词', 329, 411],
      ['高频词', 411, 492],
      ['高频词', 492, 569],
      ['高频词', 569, 650],
      ['高频词', 650, 733],
      ['中频词', 733, 817],
      ['中频词', 817, 902],
      ['中频词', 902, 986],
      ['中频词', 986, 1071],
      ['中频词', 1071, 1156],
      ['中频词', 1156, 1241],
      ['中频词', 1241, 1325],
      ['中频词', 1325, 1410],
      ['中频词', 1410, 1488],
      ['中频词', 1488, 1569],
      ['中频词', 1569, 1653],
      ['中频词', 1653, 1738],
      ['低频词', 1738, 3136],
      ['简单词', 3136, 5346],
    ],
  )
  assert.deepEqual(
    [0, 732, 733, 1737, 1738, 3135, 3136, 5345].map((index) => words[index].name),
    ['bias', 'odds', 'innovate', 'stubborn', 'skull', 'henceforth', 'beard', 'its'],
  )
  assert.ok(words.every((word) => typeof word.name === 'string' && word.name.length > 0))
  assert.ok(words.every((word) => Array.isArray(word.trans) && word.trans.length > 0))
})

test('the application catalog exposes the paper-order dictionary with its custom chapters', async () => {
  const vite = await createViteTestServer()

  try {
    const { dictionaryResources } = await vite.ssrLoadModule('/src/resources/dictionary.ts')
    const resource = dictionaryResources.find(({ id }) => id === 'shanguo-cet6-book-order')

    assert.ok(resource, '六级词汇闪过 should be visible in the dictionary catalog')
    assert.equal(resource.url, '/dicts/shanguo_cet6_book_order.json')
    assert.equal(resource.length, 5346)
    assert.equal(resource.chapters.length, 23)
  } finally {
    await vite.close()
  }
})

test('paper-defined chapter labels stay intact outside the gallery dialog', async () => {
  const vite = await createViteTestServer()

  try {
    const { getDictionaryChapterLabel } = await vite.ssrLoadModule('/src/utils/dictionaryChapter.ts')
    assert.equal(
      getDictionaryChapterLabel({ id: 'medium-1', group: '中频词', name: 'Word List 1', start: 733, end: 817 }, 9),
      '中频词 · Word List 1',
    )
    assert.equal(getDictionaryChapterLabel({ id: '3', name: '第 3 章', start: 40, end: 60 }, 2), '第 3 章')
    assert.equal(getDictionaryChapterLabel(undefined, 4), '第 5 章')
  } finally {
    await vite.close()
  }
})
