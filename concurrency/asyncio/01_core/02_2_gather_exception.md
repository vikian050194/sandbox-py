# 02_2_gather_exception

## Output

```
--- propagate ---
fetch(a) started
fetch(b) started
fetch(c) started
fetch(b) failed after 1s
raised: ValueError('b failed')
took 1.00s

fetch(c) finished after 2s
fetch(a) finished after 3s
--- collect ---
fetch(a) started
fetch(b) started
fetch(c) started
fetch(b) failed after 1s
fetch(c) finished after 2s
fetch(a) finished after 3s
results: ['a data', ValueError('b failed'), 'c data']
took 3.00s
```

## Explanation

- **`propagate`** (default `return_exceptions=False`): the exception reaches the caller after 1s. `a` and `c` aren't cancelled; they still finish after the caller has moved on. This is the gap TaskGroup closes in `03_task_group`.
- **`collect`** (`return_exceptions=True`): it waits for all three, and the exception object sits in the failed coroutine's position in the results list.
- **Pause in `main()`**: after `propagate`, `main()` waits 3s so the leftover `a` and `c` can print their output. Without that, their output would mix into the `collect` run. The wait happens after the timing is measured.
