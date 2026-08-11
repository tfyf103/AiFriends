// Turn an async task into a "single-flight" task: while one execution is pending,
// every caller receives the same Promise instead of starting duplicate work.
//
// JWT refresh is the motivating example: if 10 API requests all receive 401 at the
// same time, the browser should normally perform one refresh request, not ten.
export function createSingleFlight(task) {
  let pending = null

  return async function runSingleFlight(...args) {
    if (!pending) {
      pending = Promise.resolve()
        .then(() => task(...args))
        .finally(() => {
          pending = null
        })
    }
    return pending
  }
}
