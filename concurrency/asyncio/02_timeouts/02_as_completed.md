# 02_as_completed

## Output

```
--- plain_iterator ---
fetch(a) started
fetch(b) started
fetch(c) started
fetch(b) finished after 1s
got: b data, is original task: False
fetch(c) finished after 2s
got: c data, is original task: False
fetch(a) finished after 3s
got: a data, is original task: False
results: ['b data', 'c data', 'a data']
took 3.00s

--- async_iterator ---
fetch(a) started
fetch(b) started
fetch(c) started
fetch(b) finished after 1s
got: b -> b data, is original task: True
fetch(c) finished after 2s
got: c -> c data, is original task: True
fetch(a) finished after 3s
got: a -> a data, is original task: True
results: ['b data', 'c data', 'a data']
took 3.00s

--- with_timeout ---
fetch(a) started
fetch(b) started
fetch(c) started
fetch(b) finished after 1s
got: b -> b data
fetch(c) finished after 2s
got: c -> c data
fetch(a) cancelled
raised: ExceptionGroup('unhandled errors in a TaskGroup', [TimeoutError()])
took 2.50s
```

## Explanation

- **Order**: unlike `gather`, `as_completed` hands out results in the order the tasks finish (b, c, a), so each one can be processed as soon as it's ready.
- **`plain_iterator`**: the classic `for` form yields new awaitables, not the original tasks. The only way to know which task finished is from its result.
- **`async_iterator`** (3.13+): `async for` yields the original tasks, already done. Their names, `result()` and any other attributes are available directly.
- **`with_timeout`**: `timeout=2.5` limits the whole iteration, not each task. When it expires, `TimeoutError` leaves the `TaskGroup` block. The group cancels the task still running (`a`) and, like any error from its block, wraps it into an `ExceptionGroup`, which is why `main()` uses `except* TimeoutError`.
