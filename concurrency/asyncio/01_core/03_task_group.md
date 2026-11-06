# 03_task_group

## Output

```
--- success ---
fetch(a) started
fetch(b) started
fetch(c) started
fetch(b) finished after 1s
fetch(c) finished after 2s
fetch(a) finished after 3s
results: ['a data', 'b data', 'c data']
took 3.00s

--- failure ---
fetch(a) started
fetch(b) started
fetch(c) started
fetch(b) failed after 1s
fetch(a) cancelled
fetch(c) cancelled
raised: ExceptionGroup('unhandled errors in a TaskGroup', [ValueError('b failed')])
took 1.00s
```

## Explanation

- **`success`**: the tasks are started with `tg.create_task(...)`. Leaving the `async with` block waits for all of them, and the results are read afterwards with `task.result()`.
- **`failure`**: when `b` fails, the group cancels `a` and `c`, so nothing keeps running in the background. That's why `main()` doesn't need the 3s pause from `02_2_gather_exception`. The error arrives wrapped in an `ExceptionGroup`.
- **Cancellation**: `fetch` catches `asyncio.CancelledError` to print "cancelled" and then re-raises it. If it didn't re-raise, the task wouldn't be marked as cancelled.

`main()` catches the error with a plain `except ExceptionGroup`. `except*`, which can handle different error types separately inside one group, is covered in `04_exception_group`.
