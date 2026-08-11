import { readFile, readdir } from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const scanRoots = [path.join(root, 'src'), path.join(root, 'scripts'), path.join(root, 'tests')]
const extensions = new Set(['.js', '.mjs', '.vue'])
const problems = []

async function walk(dir) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name)
    if (entry.isDirectory()) {
      await walk(full)
      continue
    }
    if (!extensions.has(path.extname(entry.name))) continue

    const text = await readFile(full, 'utf8')
    const lines = text.split('\n')
    lines.forEach((line, index) => {
      if (/\s+$/.test(line) && line.length > 0) {
        problems.push(`${path.relative(root, full)}:${index + 1} trailing whitespace`)
      }
      if (line.includes('\t')) {
        problems.push(`${path.relative(root, full)}:${index + 1} tab character`)
      }
    })
  }
}

for (const dir of scanRoots) {
  await walk(dir)
}

if (problems.length) {
  console.error(problems.join('\n'))
  process.exit(1)
}

console.log('✓ frontend quality check passed')
