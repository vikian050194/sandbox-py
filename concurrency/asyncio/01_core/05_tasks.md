# 05_tasks

## Output

```
--- background ---
task created, done: False
fetch(a) started
main did other work for 1s, done: False
fetch(a) finished after 2s
task awaited, done: True
results: a data
took 2.00s

--- cancel ---
fetch(a) started
cancel requested, done: False
fetch(a) cancelled
task cancelled: True
results: None
took 1.00s

--- uncancel ---
stubborn_fetch(a) started
stubborn_fetch(a) cancel requested, cancelling() = 1
stubborn_fetch(a) ignores cancellation and retries
stubborn_fetch(a) finished
results: a data
took 1.50s
```

## Explanation

- **`background`**: `create_task` doesn't start the coroutine immediately. `fetch(a) started` appears only after `main` reaches its first `await`. While `main` sleeps for 1s, the task runs in the background. `await task` then waits for the remaining 1s and returns the result, so the total is 2s, not 3s.
- **`cancel`**: `task.cancel()` only requests cancellation, so the task isn't done right after the call. `CancelledError` is thrown into the task at the `await` where it's suspended. `fetch` re-raises it, the task becomes cancelled, and awaiting it raises `CancelledError` in the caller.
- **`uncancel`**: `task.cancelling()` counts pending `cancel()` requests, and `task.uncancel()` decrements it. If the count drops to 0, nobody else wants the task cancelled, so the coroutine can swallow the cancellation and retry. That's why the run takes 1.5s: 0.5s before the cancel, then another 1s retry.

Swallowing cancellation is generally a bad idea. `uncancel()` exists mainly for building tools like `asyncio.timeout` and `TaskGroup`, which cancel a task internally and must turn that back into a normal state without hiding a real external `cancel()`.
