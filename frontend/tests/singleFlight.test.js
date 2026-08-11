import test from 'node:test'
import assert from 'node:assert/strict'

import { createSingleFlight } from '../src/js/utils/singleFlight.js'

test('concurrent callers share one pending task', async () => {
  let calls = 0
  const run = createSingleFlight(async () => {
    calls++
    await new Promise(resolve => setTimeout(resolve, 20))
    return 'token-2'
  })

  const results = await Promise.all([run(), run(), run()])
  assert.equal(calls, 1)
  assert.deepEqual(results, ['token-2', 'token-2', 'token-2'])
})

test('a rejected task is cleared so the next call can retry', async () => {
  let calls = 0
  const run = createSingleFlight(async () => {
    calls++
    if (calls === 1) throw new Error('first refresh failed')
    return 'token-ok'
  })

  await assert.rejects(run(), /first refresh failed/)
  assert.equal(await run(), 'token-ok')
  assert.equal(calls, 2)
})
