import { chromium } from '@playwright/test'
import assert from 'node:assert/strict'
import { mkdir } from 'node:fs/promises'
import path from 'node:path'

const baseUrl = process.argv[2] ?? 'http://127.0.0.1:4173'
const outputDir = process.argv[3] ?? 'tmp/ui-verification'

await mkdir(outputDir, { recursive: true })

const browser = await chromium.launch({ headless: true })
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } })
  await page.goto(`${baseUrl}/gallery`, { waitUntil: 'networkidle' })

  const card = page.getByText('六级词汇闪过（纸书同序）', { exact: true })
  assert.equal(await card.count(), 1, 'the paper-order dictionary card should be visible once')
  assert.match(await card.locator('xpath=..').innerText(), /5346 词/)
  await page.screenshot({ path: path.join(outputDir, 'shanguo-catalog.png'), fullPage: true })

  await card.click()
  const dialog = page.getByRole('dialog')
  await dialog.waitFor()
  const dialogText = await dialog.innerText()

  assert.match(dialogText, /23 章节/)
  assert.match(dialogText, /高频词 · 82 词/)
  assert.match(dialogText, /中频词 · 85 词/)
  assert.match(dialogText, /低频词 · 1398 词/)
  assert.match(dialogText, /简单词 · 2210 词/)
  await page.screenshot({ path: path.join(outputDir, 'shanguo-chapters.png'), fullPage: true })

  await dialog.getByText('Word List 1', { exact: true }).nth(1).click()
  await page.waitForURL(`${baseUrl}/`)
  await page.waitForFunction(() => document.body.textContent?.includes('innovate'))
  const typingText = await page.locator('body').innerText()
  const typingTextContent = await page.locator('body').textContent()
  assert.match(typingText, /中频词 · Word List 1/)
  assert.match(typingTextContent ?? '', /innovate/)
  await page.screenshot({ path: path.join(outputDir, 'shanguo-after-medium-click.png'), fullPage: true })
  assert.match(typingText, /六级词汇闪过（纸书同序）/)
  await page.screenshot({ path: path.join(outputDir, 'shanguo-medium-word-list-1.png'), fullPage: true })

  console.log('Verified catalog, 23 chapter cards, and Medium Word List 1 starting with innovate.')
} finally {
  await browser.close()
}
