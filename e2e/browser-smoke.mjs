import { chromium } from 'playwright'
import { spawn, spawnSync } from 'node:child_process'
import { mkdirSync, rmSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const here = path.dirname(fileURLToPath(import.meta.url))
const root = path.resolve(here, '..')
const tmpDir = path.join(here, '.tmp')
const artifactsDir = path.join(here, 'artifacts')
const python = process.env.PYTHON || 'python'
const npm = process.platform === 'win32' ? 'npm.cmd' : 'npm'

const env = {
  ...process.env,
  DJANGO_DEBUG: 'true',
  DJANGO_SECRET_KEY: 'browser-e2e-development-only-key-please-do-not-use-in-production',
  DJANGO_ALLOWED_HOSTS: '127.0.0.1,localhost',
  CORS_ALLOWED_ORIGINS: 'http://127.0.0.1:5173,http://localhost:5173',
  DATABASE_PATH: path.join(tmpDir, 'e2e.sqlite3'),
  MEDIA_ROOT: path.join(tmpDir, 'media'),
  AI_MODE: 'mock',
  ENABLE_RAG: 'false',
  ENABLE_ASR: 'false',
  ENABLE_TTS: 'false',
}

function runOrFail(command, args, options = {}) {
  const result = spawnSync(command, args, {
    cwd: root,
    env,
    stdio: 'inherit',
    ...options,
  })
  if (result.status !== 0) {
    throw new Error(`${command} ${args.join(' ')} failed with status ${result.status}`)
  }
}

async function waitForUrl(url, label, timeoutMs = 45_000) {
  const deadline = Date.now() + timeoutMs
  let lastError = null
  while (Date.now() < deadline) {
    try {
      const response = await fetch(url)
      if (response.ok) return
      lastError = new Error(`${label} returned HTTP ${response.status}`)
    } catch (error) {
      lastError = error
    }
    await new Promise(resolve => setTimeout(resolve, 500))
  }
  throw new Error(`Timed out waiting for ${label}: ${lastError ?? 'unknown error'}`)
}

function start(command, args, cwd) {
  return spawn(command, args, {
    cwd,
    env,
    stdio: 'inherit',
  })
}

function stop(child) {
  if (!child || child.killed) return
  child.kill('SIGTERM')
}

async function main() {
  rmSync(tmpDir, { recursive: true, force: true })
  rmSync(artifactsDir, { recursive: true, force: true })
  mkdirSync(tmpDir, { recursive: true })
  mkdirSync(artifactsDir, { recursive: true })

  runOrFail(python, ['backend/manage.py', 'migrate', '--noinput'])

  const backend = start(
    python,
    ['backend/manage.py', 'runserver', '127.0.0.1:8000', '--noreload'],
    root,
  )
  const frontend = start(
    npm,
    ['run', 'dev', '--', '--host', '127.0.0.1', '--port', '5173'],
    path.join(root, 'frontend'),
  )

  let browser
  try {
    await Promise.all([
      waitForUrl('http://127.0.0.1:8000/api/health/', 'Django health endpoint'),
      waitForUrl('http://127.0.0.1:5173/', 'Vite frontend'),
    ])

    browser = await chromium.launch({ headless: true })
    const context = await browser.newContext({
      viewport: { width: 1280, height: 900 },
      locale: 'en-US',
    })
    const page = await context.newPage()

    // 1. Verify project identity rather than the scaffold default.
    await page.goto('http://127.0.0.1:5173/', { waitUntil: 'networkidle' })
    if ((await page.title()) !== 'AiFriends') {
      throw new Error(`Expected browser title AiFriends, got ${JSON.stringify(await page.title())}`)
    }

    // 2. Exercise a real browser → Vite proxy → Django → SQLite registration flow.
    await page.goto('http://127.0.0.1:5173/user/account/register', {
      waitUntil: 'networkidle',
    })
    const username = `e2e_${Date.now()}`
    await page.getByPlaceholder('用户名', { exact: true }).fill(username)
    await page.getByPlaceholder('密码', { exact: true }).fill('e2e-password-123')
    await page.getByPlaceholder('确认密码', { exact: true }).fill('e2e-password-123')
    await page.getByRole('button', { name: '注册', exact: true }).click()
    await page.waitForURL('http://127.0.0.1:5173/', { timeout: 15_000 })

    // 3. Prove the newly authenticated browser can enter a protected route.
    await page.goto('http://127.0.0.1:5173/friend', { waitUntil: 'networkidle' })
    if (!page.url().endsWith('/friend')) {
      throw new Error(`Expected authenticated /friend route, got ${page.url()}`)
    }

    // 4. Reload to exercise the maintained refresh/session-restoration path.
    await page.reload({ waitUntil: 'networkidle' })
    await page.waitForTimeout(1200)
    if (!page.url().endsWith('/friend')) {
      throw new Error(`Auth state was not restored after reload; got ${page.url()}`)
    }

    await page.screenshot({
      path: path.join(artifactsDir, 'authenticated-friend.png'),
      fullPage: true,
    })

    console.log('Browser E2E passed:')
    console.log('  - AiFriends browser title')
    console.log('  - registration through the real API proxy')
    console.log('  - protected Friend route access')
    console.log('  - auth restoration after reload')
    console.log('  - AI_MODE=mock; no external AI credentials used')
  } finally {
    if (browser) await browser.close()
    stop(frontend)
    stop(backend)
  }
}

main().catch(error => {
  console.error(error)
  process.exitCode = 1
})
