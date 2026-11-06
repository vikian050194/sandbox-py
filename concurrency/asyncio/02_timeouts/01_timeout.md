# 01_timeout

## Output

```
--- block_in_time ---
fetch(a) started
fetch(a) finished after 1s
fetch(b) started
fetch(b) finished after 1s
results: ['a data', 'b data']
took 2.00s

--- block_expired ---
fetch(a) started
fetch(a) finished after 2s
fetch(b) started
fetch(b) cancelled
deadline expired: True
raised: TimeoutError()
took 3.00s

--- reschedule ---
deadline set to 1s from now
fetch(a) started
fetch(a) cancelled
raised: TimeoutError()
took 1.00s

--- wait_for_expired ---
fetch(a) started
fetch(a) cancelled
raised: TimeoutError()
took 2.00s
```

## Explanation

- **`block_in_time`**: `asyncio.timeout(3)` sets one deadline for the whole block. Two 1s awaits fit into it.
- **`block_expired`**: the deadline is shared by everything in the block. `a` uses 2s, so `b` has only 1s left and gets cancelled at 3s. Inside the block the coroutine sees `CancelledError`; on exit from the block it's converted to `TimeoutError`. `cm.expired()` tells whether the timeout fired.
- **`reschedule`**: the deadline can be `None` (no limit) at the start and set or moved later with `cm.reschedule(...)`. It takes an absolute time from `loop.time()`, not a duration.
- **`wait_for_expired`**: the older API. It limits one awaitable, not a block of code, and cancels that awaitable when time runs out.

Since 3.11, `asyncio.TimeoutError` is just an alias of the built-in `TimeoutError`, so `except TimeoutError` catches both.
