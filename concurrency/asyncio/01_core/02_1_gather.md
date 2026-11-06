# 02_1_gather

## Output

```
--- sequential ---
fetch(a) started
fetch(a) finished after 1s
fetch(b) started
fetch(b) finished after 2s
fetch(c) started
fetch(c) finished after 3s
results: ['a data', 'b data', 'c data']
took 6.01s

--- concurrent ---
fetch(a) started
fetch(b) started
fetch(c) started
fetch(b) finished after 1s
fetch(c) finished after 2s
fetch(a) finished after 3s
results: ['a data', 'b data', 'c data']
took 3.00s
```

## Explanation

- **`sequential`**: awaiting the calls one by one in a loop means the waits add up: 1 + 2 + 3 = 6s.
- **`concurrent`**: `asyncio.gather` wraps every coroutine into a task and schedules them all at once, so the total time is the longest wait (3s).
- **Result order**: in `concurrent` the delays are given in a different order (`a`=3, `b`=1, `c`=2), so they finish as b, c, a. `gather` still returns the results in the order they were passed, not the order they finished.
