import { access, cp, mkdir, readdir } from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const here = path.dirname(fileURLToPath(import.meta.url))
const frontendRoot = path.resolve(here, '..')
const targetRoot = path.join(frontendRoot, 'public', 'vad')
const targetOnnx = path.join(targetRoot, 'onnx')
const vadDist = path.join(frontendRoot, 'node_modules', '@ricky0123', 'vad-web', 'dist')

const ortCandidates = [
  path.join(frontendRoot, 'node_modules', 'onnxruntime-web', 'dist'),
  path.join(
    frontendRoot,
    'node_modules',
    '@ricky0123',
    'vad-web',
    'node_modules',
    'onnxruntime-web',
    'dist',
  ),
]

async function firstExisting(paths) {
  for (const candidate of paths) {
    try {
      await access(candidate)
      return candidate
    } catch {
      // npm may hoist the dependency or keep it nested. Try both layouts.
    }
  }
  return null
}

const ortDist = await firstExisting(ortCandidates)
if (!ortDist) {
  throw new Error('找不到 onnxruntime-web。请先运行 npm install / npm ci。')
}

await mkdir(targetRoot, { recursive: true })
await mkdir(targetOnnx, { recursive: true })

const vadFiles = new Set([
  'vad.worklet.bundle.min.js',
  'silero_vad_v5.onnx',
  'silero_vad_legacy.onnx',
])

let copiedVad = 0
for (const name of await readdir(vadDist)) {
  if (vadFiles.has(name)) {
    await cp(path.join(vadDist, name), path.join(targetRoot, name))
    copiedVad++
  }
}

let copiedOnnx = 0
for (const name of await readdir(ortDist)) {
  if ((name.startsWith('ort-wasm') && name.endsWith('.wasm')) || name.endsWith('.mjs')) {
    await cp(path.join(ortDist, name), path.join(targetOnnx, name))
    copiedOnnx++
  }
}

if (copiedVad === 0 || copiedOnnx === 0) {
  throw new Error(
    `VAD 资源不完整：vad=${copiedVad}, onnx=${copiedOnnx}。请检查依赖版本。`,
  )
}

console.log(`✓ VAD assets ready: ${targetRoot}`)
console.log(`✓ VAD files: ${copiedVad}`)
console.log(`✓ ONNX Runtime files: ${copiedOnnx}`)
