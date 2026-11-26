import fs from 'node:fs/promises'
import path from 'node:path'
import { chromium } from '@playwright/test'

const DESKTOP = 'C:\\Users\\hp\\Desktop'
const CET6_DIR = path.join(DESKTOP, '每日英语文章')
const KAOYAN_DIR = path.join(DESKTOP, '23考研英语词汇闪过_每日英语文章')
const PDF_OUT_DIR = path.join(DESKTOP, '英语阅读文章_PDF汇总')

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

function formatInline(text) {
  let s = escapeHtml(text)
  // Bold **word**
  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
  // Code `code`
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>')
  return s
}

function markdownToHtmlBody(mdText) {
  const lines = mdText.split(/\r?\n/)
  const html = []
  let inList = false
  let inTable = false
  let tableHeaderDone = false

  const closeList = () => {
    if (inList) {
      html.push('</ul>')
      inList = false
    }
  }
  const closeTable = () => {
    if (inTable) {
      html.push('</tbody></table>')
      inTable = false
      tableHeaderDone = false
    }
  }

  for (let i = 0; i < lines.length; i++) {
    const raw = lines[i]
    const s = raw.trim()

    if (!s) {
      closeList()
      closeTable()
      continue
    }

    // Skip any residual blockquote disclaimer
    if (s.startsWith('>')) {
      continue
    }

    if (s.startsWith('# ')) {
      closeList()
      closeTable()
      html.push(`<h1>${formatInline(s.slice(2).trim())}</h1>`)
      continue
    }

    if (s.startsWith('## ')) {
      closeList()
      closeTable()
      const h2Text = s.slice(3).trim()
      const isEngTitle = /^[A-Za-z0-9\s,'’\-?!:]+$/.test(h2Text)
      if (isEngTitle) {
        html.push(`<h2 class="article-title">${formatInline(h2Text)}</h2>`)
      } else {
        html.push(`<h2 class="section-title">${formatInline(h2Text)}</h2>`)
      }
      continue
    }

    if (s.startsWith('|') && s.endsWith('|')) {
      closeList()
      const cells = s
        .slice(1, -1)
        .split('|')
        .map((c) => c.trim())
      // Check if separator row | --- | --- |
      if (cells.every((c) => /^:?-{2,}:?$/.test(c))) {
        continue
      }
      if (!inTable) {
        inTable = true
        tableHeaderDone = false
        html.push('<table><thead><tr>')
        for (const c of cells) {
          html.push(`<th>${formatInline(c)}</th>`)
        }
        html.push('</tr></thead><tbody>')
        tableHeaderDone = true
      } else {
        html.push('<tr>')
        for (const c of cells) {
          html.push(`<td>${formatInline(c)}</td>`)
        }
        html.push('</tr>')
      }
      continue
    }

    closeTable()

    if (s.startsWith('- ')) {
      if (!inList) {
        inList = true
        html.push('<ul class="options-list">')
      }
      html.push(`<li>${formatInline(s.slice(2).trim())}</li>`)
      continue
    }

    closeList()

    // Numbered question or sentence item
    if (/^\d+\.\s+/.test(s)) {
      html.push(`<p class="numbered-item">${formatInline(s)}</p>`)
      continue
    }

    // Paragraph [P1]..[P6]
    if (/^\[P\d+\]/.test(s)) {
      const m = s.match(/^(\[P\d+\])\s*(.*)$/)
      if (m) {
        html.push(
          `<p class="reading-para"><span class="para-tag">${escapeHtml(m[1])}</span> ${formatInline(m[2])}</p>`,
        )
        continue
      }
    }

    html.push(`<p>${formatInline(s)}</p>`)
  }

  closeList()
  closeTable()
  return html.join('\n')
}

function wrapHtmlDocument(bodyHtml, title) {
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<title>${escapeHtml(title)}</title>
<style>
  @page {
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
  }
  body {
    font-family: "Times New Roman", "Noto Serif SC", "Source Han Serif SC", "Microsoft YaHei", "PingFang SC", serif;
    font-size: 11pt;
    line-height: 1.68;
    color: #111827;
    margin: 0;
    padding: 0;
  }
  h1 {
    font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
    font-size: 15pt;
    font-weight: 700;
    color: #1e293b;
    margin: 0 0 4pt 0;
    border-bottom: 1.5pt solid #334155;
    padding-bottom: 4pt;
  }
  h2.article-title {
    font-family: "Times New Roman", Georgia, serif;
    font-size: 16pt;
    font-weight: 700;
    color: #0f172a;
    margin: 8pt 0 12pt 0;
  }
  h2.section-title {
    font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
    font-size: 12.5pt;
    font-weight: 700;
    color: #1e3a8a;
    margin: 16pt 0 8pt 0;
    padding-left: 6pt;
    border-left: 3pt solid #2563eb;
    page-break-after: avoid;
  }
  p {
    margin: 0 0 8pt 0;
    text-align: justify;
  }
  p.reading-para {
    font-size: 11.2pt;
    line-height: 1.72;
    margin-bottom: 9pt;
  }
  span.para-tag {
    font-family: Consolas, monospace;
    font-size: 9.5pt;
    font-weight: 700;
    color: #475569;
    margin-right: 4pt;
  }
  strong {
    font-weight: 700;
    color: #000000;
    text-decoration: underline;
    text-decoration-color: #64748b;
    text-underline-offset: 2px;
  }
  p.numbered-item {
    font-weight: 600;
    margin-top: 8pt;
    margin-bottom: 3pt;
    page-break-after: avoid;
  }
  ul.options-list {
    list-style: none;
    padding-left: 14pt;
    margin: 0 0 8pt 0;
  }
  ul.options-list li {
    margin-bottom: 2.5pt;
    line-height: 1.55;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 6pt 0 12pt 0;
    font-size: 9.5pt;
    font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
  }
  th, td {
    border: 0.75pt solid #cbd5e1;
    padding: 4pt 6pt;
    text-align: left;
    vertical-align: top;
    line-height: 1.45;
  }
  th {
    background-color: #f1f5f9;
    font-weight: 700;
    color: #1e293b;
  }
  tr {
    page-break-inside: avoid;
  }
</style>
</head>
<body>
${bodyHtml}
</body>
</html>`
}

async function collectMarkdownFiles(baseDir, bookTag) {
  const results = []
  const entries = await fs.readdir(baseDir, { withFileTypes: true })

  // Sort day folders in logical study order: 高频词 -> 中频词 -> 低频词 -> 偶考词 -> 简单词 -> 补充词, then by day number
  const groupRank = { 高频词: 1, 中频词: 2, 低频词: 3, 偶考词: 4, 简单词: 5, 补充词: 6 }
  const dayDirs = entries
    .filter((e) => e.isDirectory() && e.name !== '旧版')
    .map((e) => {
      const m = e.name.match(/^(高频词|中频词|低频词|偶考词|简单词|补充词)第(\d+)天$/)
      return {
        name: e.name,
        group: m ? m[1] : e.name,
        day: m ? Number(m[2]) : 999,
        rank: m ? groupRank[m[1]] ?? 9 : 9,
      }
    })
    .sort((a, b) => a.rank - b.rank || a.day - b.day)

  for (const d of dayDirs) {
    const dirPath = path.join(baseDir, d.name)
    for (const artNum of [1, 2]) {
      const fName = `英语文章${artNum}.md`
      const fPath = path.join(dirPath, fName)
      try {
        await fs.access(fPath)
        const padDay = String(d.day).padStart(2, '0')
        const outPdfName = `${bookTag}_${d.group}第${padDay}天_英语文章${artNum}.pdf`
        results.push({
          bookTag,
          group: d.group,
          day: d.day,
          artNum,
          mdPath: fPath,
          subFolder: path.join(PDF_OUT_DIR, bookTag, d.name),
          subPdfPath: path.join(PDF_OUT_DIR, bookTag, d.name, `英语文章${artNum}.pdf`),
          flatPdfPath: path.join(PDF_OUT_DIR, '全部文章平铺汇总', outPdfName),
        })
      } catch {
        // skip
      }
    }
  }
  return results
}

async function main() {
  await fs.mkdir(PDF_OUT_DIR, { recursive: true })
  await fs.mkdir(path.join(PDF_OUT_DIR, '全部文章平铺汇总'), { recursive: true })

  const kaoyanItems = await collectMarkdownFiles(KAOYAN_DIR, '23考研词汇闪过')
  const cet6Items = await collectMarkdownFiles(CET6_DIR, '六级词汇闪过')
  const dailyOnly = process.argv.includes('--daily-only')
  const allItems = [...kaoyanItems, ...cet6Items]

  console.log(`Found ${kaoyanItems.length} Kaoyan articles and ${cet6Items.length} CET-6 articles (total ${allItems.length}).`)

  const browser = await chromium.launch({ headless: true })
  const CONCURRENCY = 6
  const pages = await Promise.all(Array.from({ length: CONCURRENCY }, () => browser.newPage()))

  // Group Kaoyan articles by study day (each day = 1 PDF containing Article 1 + Article 2)
  const dailyGroups = []
  for (let i = 0; i < kaoyanItems.length; i += 2) {
    dailyGroups.push({
      seq: i / 2 + 1,
      group: kaoyanItems[i].group,
      day: kaoyanItems[i].day,
      items: kaoyanItems.slice(i, i + 2),
    })
  }

  const dailyDirName = `23考研词汇闪过_每日PDF（共${dailyGroups.length}天）`
  const dailyOutDir = path.join(PDF_OUT_DIR, dailyDirName)
  // Remove older daily PDF folders with previous day counts
  for (const name of await fs.readdir(PDF_OUT_DIR)) {
    if (name.startsWith('23考研词汇闪过_每日PDF（') && name !== dailyDirName && !name.endsWith('.zip')) {
      await fs.rm(path.join(PDF_OUT_DIR, name), { recursive: true, force: true }).catch(() => {})
    }
  }
  await fs.mkdir(dailyOutDir, { recursive: true })

  let dailyDone = 0
  let dailyCursor = 0
  await Promise.all(
    pages.map(async (page) => {
      while (dailyCursor < dailyGroups.length) {
        const dg = dailyGroups[dailyCursor++]
        const bodies = []
        for (let k = 0; k < dg.items.length; k++) {
          const mdText = await fs.readFile(dg.items[k].mdPath, 'utf8')
          const brk = k < dg.items.length - 1 ? ' style="page-break-after: always;"' : ''
          bodies.push(`<div${brk}>${markdownToHtmlBody(mdText)}</div>`)
        }
        const padSeq = String(dg.seq).padStart(2, '0')
        const padDay = String(dg.day).padStart(2, '0')
        const title = `第${padSeq}天_${dg.group}第${padDay}天`
        const html = wrapHtmlDocument(bodies.join('\n'), title)
        await page.setContent(html, { waitUntil: 'load' })
        await page.pdf({
          path: path.join(dailyOutDir, `${title}.pdf`),
          format: 'A4',
          printBackground: true,
        })
        dailyDone += 1
        if (dailyDone % 15 === 0 || dailyDone === dailyGroups.length) {
          console.log(`Generated daily PDFs: ${dailyDone} / ${dailyGroups.length}`)
        }
      }
    }),
  )
  console.log(`Daily PDF folder ready: ${dailyOutDir}`)

  if (dailyOnly) {
    await browser.close()
    return
  }

  let completed = 0
  async function processItem(page, item) {
    const mdText = await fs.readFile(item.mdPath, 'utf8')
    const bodyHtml = markdownToHtmlBody(mdText)
    const fullHtml = wrapHtmlDocument(bodyHtml, `${item.bookTag} - ${item.group}第${item.day}天 - 文章${item.artNum}`)

    await page.setContent(fullHtml, { waitUntil: 'load' })
    await fs.mkdir(item.subFolder, { recursive: true })
    const pdfBuffer = await page.pdf({
      format: 'A4',
      printBackground: true,
    })
    await fs.writeFile(item.subPdfPath, pdfBuffer)
    await fs.writeFile(item.flatPdfPath, pdfBuffer)
    // Also save PDF right next to the original markdown file so user sees it in the original folders too!
    const sideBySidePdf = item.mdPath.replace(/\.md$/, '.pdf')
    await fs.writeFile(sideBySidePdf, pdfBuffer)

    completed += 1
    if (completed % 20 === 0 || completed === allItems.length) {
      console.log(`Converted ${completed} / ${allItems.length} PDFs...`)
    }
  }

  // Worker pool
  let cursor = 0
  await Promise.all(
    pages.map(async (page) => {
      while (cursor < allItems.length) {
        const idx = cursor++
        await processItem(page, allItems[idx])
      }
    }),
  )

  // Clean up any older combined Kaoyan PDFs with a previous day/article count
  const existingOutFiles = await fs.readdir(PDF_OUT_DIR)
  const currentKaoyanLabel = `23考研词汇闪过_阅读合集（前${kaoyanItems.length / 2}天${kaoyanItems.length}篇）`
  for (const name of existingOutFiles) {
    if (name.startsWith('23考研词汇闪过_阅读合集（') && name !== `${currentKaoyanLabel}.pdf`) {
      await fs.unlink(path.join(PDF_OUT_DIR, name)).catch(() => {})
    }
  }

  // Also create 2 combined compilation PDFs (one for 23考研词汇闪过, one for 六级词汇闪过) for easy continuous reading
  const mainPage = pages[0]
  for (const [bookLabel, items] of [
    [currentKaoyanLabel, kaoyanItems],
    ['六级词汇闪过_阅读合集（52天104篇）', cet6Items],
  ]) {
    const bodies = []
    for (const item of items) {
      const mdText = await fs.readFile(item.mdPath, 'utf8')
      bodies.push(`<div style="page-break-after: always;">${markdownToHtmlBody(mdText)}</div>`)
    }
    const combinedHtml = wrapHtmlDocument(bodies.join('\n'), bookLabel)
    await mainPage.setContent(combinedHtml, { waitUntil: 'load' })
    const combinedPdfPath = path.join(PDF_OUT_DIR, `${bookLabel}.pdf`)
    await mainPage.pdf({
      path: combinedPdfPath,
      format: 'A4',
      printBackground: true,
    })
    console.log(`Generated combined PDF: ${combinedPdfPath}`)
  }

  await browser.close()
  console.log('All PDFs generated successfully!')
}

main().catch((err) => {
  console.error(err)
  process.exit(1)
})
