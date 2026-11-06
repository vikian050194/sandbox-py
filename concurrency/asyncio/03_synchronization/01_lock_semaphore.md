# 01_lock_semaphore

## Output

```
--- no_lock ---
increment(a) 0 -> 1
increment(b) 0 -> 1
increment(c) 0 -> 1
increment(d) 0 -> 1
increment(e) 0 -> 1
results: 1
took 0.10s

--- with_lock ---
increment(a) 0 -> 1
increment(b) 1 -> 2
increment(c) 2 -> 3
increment(d) 3 -> 4
increment(e) 4 -> 5
results: 5
took 0.50s

--- limited_downloads ---
download(a) started, active: ['a']
download(b) started, active: ['a', 'b']
download(a) finished
download(b) finished
download(c) started, active: ['c']
download(d) started, active: ['c', 'd']
download(c) finished
download(d) finished
download(e) started, active: ['e']
download(f) started, active: ['e', 'f']
download(e) finished
download(f) finished
results: ['a data', 'b data', 'c data', 'd data', 'e data', 'f data']
took 3.00s
```

## Explanation

- **`no_lock`**: asyncio runs one coroutine at a time, but a coroutine can be paused at any `await`. Here every `increment` reads the value, awaits, and only then writes. All five read `0` before any of them writes, so 4 of the 5 updates are lost. `contextlib.nullcontext()` is only a do-nothing stand-in, so both runners can share the same `async with` code.
- **`with_lock`**: `asyncio.Lock` lets only one coroutine into the block at a time, so every read-modify-write completes before the next starts. The result is correct, but the work becomes sequential (0.5s instead of 0.1s).
- **`limited_downloads`**: `asyncio.Semaphore(2)` is a lock that up to 2 coroutines can hold at once. Six 1s downloads run in three waves of two, so they take 3s, and at most two are active at any moment.

Race conditions in asyncio only happen at `await` points. Code between two awaits always runs without interruption, so a read-modify-write with no `await` in the middle needs no lock.
