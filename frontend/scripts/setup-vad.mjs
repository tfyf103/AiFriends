import { cp, mkdir, readdir } from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const here = path.dirname(fileURLToPath(import.meta.url))
const frontendRoot = path.resolve(here, '..')
const targetRoot = path.join(frontendRoot, 'public', 'vad')
const targetOnnx = path.join(targetRoot, 'onnx')
const vadDist = path.join(frontendRoot, 'node_modules', '@ricky0123', 'vad-web', 'dist')
const ortDist = path.join(frontendRoot, 'node_modules', 'onnxruntime-web', 'dist')

await mkdir(targetRoot, { recursive: true })
await mkdir(targetOnnx, { recursive: true })

const vadFiles = new Set([
  'vad.worklet.bundle.min.js',
  'silero_vad_v5.onnx',
  'silero_vad_legacy.onnx',
])

let copied = 0
for (const name of await readdir(vadDist)) {
  if (vadFiles.has(name)) {
    await cp(path.join(vadDist, name), path.join(targetRoot, name))
    copied++
  }
}

for (const name of await readdir(ortDist)) {
  if ((name.startsWith('ort-wasm') && name.endsWith('.wasm')) || name.endsWith('.mjs')) {
    await cp(path.join(ortDist, name), path.join(targetOnnx, name))
    copied++
  }
}

if (copied === 0) {
  throw new Error('没有找到 VAD/ONNX Runtime 资源。请先运行 npm install。')
}

console.log(`✓ VAD assets ready: ${targetRoot}`)
console.log(`✓ copied ${copied} files`)
