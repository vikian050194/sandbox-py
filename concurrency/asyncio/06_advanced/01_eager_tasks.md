# 01_eager_tasks

## Output

```
--- lazy ---
creating task a
task a created, done: False
creating task b
task b created, done: False
fetch(a) started
fetch(a) cache hit
fetch(b) started
fetch(b) finished
results: ['a data (cached)', 'b data']

--- eager_start ---
creating task a
fetch(a) started
fetch(a) cache hit
task a created, done: True
creating task b
fetch(b) started
task b created, done: False
fetch(b) finished
results: ['a data (cached)', 'b data']

--- eager_factory ---
creating task a
fetch(a) started
fetch(a) cache hit
task a created, done: True
creating task b
fetch(b) started
task b created, done: False
fetch(b) finished
results: ['a data (cached)', 'b data']
```

## Explanation

- **`lazy`** (default): `create_task` only schedules the coroutine. Both tasks are created first, and `fetch` starts only when the creating coroutine reaches an `await`.
- **`eager_start`** (3.14): `create_task(..., eager_start=True)` starts running the coroutine immediately, inside the `create_task` call, up to its first real `await`. For `a` (cache hit) the coroutine finishes without ever awaiting, so the task is already done when `create_task` returns and is never scheduled on the loop. `b` runs up to `asyncio.sleep` and continues on the loop as usual.
- **`eager_factory`** (3.12+): `loop.set_task_factory(asyncio.eager_task_factory)` makes all new tasks on the loop eager. `eager_start` must not be passed at all in this case; even `eager_start=None` overrides the factory's default and makes the task lazy again.

Eager tasks save scheduling overhead when many tasks complete synchronously (caches, already available data). The downside is that the order of execution changes: code in the coroutine runs before the code after `create_task`, which can surprise code written with lazy tasks in mind.
