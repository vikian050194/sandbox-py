# 02_barrier

## Output

```
--- meet ---
worker(a) preparing for 3s
worker(b) preparing for 1s
worker(c) preparing for 2s
worker(b) ready, waiting for others (0 already waiting)
worker(c) ready, waiting for others (1 already waiting)
worker(a) ready, waiting for others (2 already waiting)
worker(a) passed the barrier with index 2
worker(b) passed the barrier with index 0
worker(c) passed the barrier with index 1
results: [2, 0, 1]
took 3.00s

--- broken ---
worker(a) preparing for 3s
worker(b) preparing for 1s
worker(c) preparing for 2s
worker(b) ready, waiting for others (0 already waiting)
worker(c) ready, waiting for others (1 already waiting)
worker(a) failed, aborting barrier
worker(b) barrier is broken
worker(c) barrier is broken
handled ValueError: (ValueError('a failed'),)
handled BrokenBarrierError: (BrokenBarrierError('Abort or reset of barrier'), BrokenBarrierError('Abort or reset of barrier'))
took 3.00s
```

## Explanation

- **`meet`**: `asyncio.Barrier(3)` blocks every `wait()` call until 3 coroutines are waiting, then releases all of them together. Workers finish preparing at 1s, 2s and 3s, but all pass the barrier at 3s. `wait()` returns a unique index from 0 to 2 in arrival order, which can be used to pick one coroutine for a one-time job, e.g. `if index == 0`.
- **`broken`**: `a` fails before reaching the barrier and calls `barrier.abort()`. The barrier becomes broken, so the waiting workers `b` and `c` get `BrokenBarrierError` instead of hanging forever. All three errors end up in the TaskGroup's `ExceptionGroup`, and both `except*` clauses run.

A barrier can be reused: after it releases a full set of coroutines, it resets itself for the next round. `barrier.reset()` returns a broken barrier to its initial state.
