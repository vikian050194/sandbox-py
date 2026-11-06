# 01_cpu_bound

## Output

Regular build (`python3.14`):

```
free-threaded build: False
GIL enabled: True

--- sequential ---
results: [17984, 17984, 17984, 17984]
took 1.51s

--- threads ---
results: [17984, 17984, 17984, 17984]
took 1.48s
```

Free-threaded build (`python3.14t`): not run yet, it's not installed (`pyenv install 3.14.2t`).

## Explanation

- **Regular build**: the GIL (global interpreter lock) lets only one thread execute Python bytecode at a time. Four threads doing pure Python CPU work take turns, so they take about as long as running the same work sequentially (~1.5s both).
- **Free-threaded build** (`python3.14t`): built without the GIL. Since 3.14 it's officially supported (PEP 779), no longer experimental. The same four threads can run on four cores, so `threads` is expected to be roughly 4× faster than `sequential`. Single-threaded code is somewhat slower on this build.
- **Checking the state**: `sysconfig.get_config_var('Py_GIL_DISABLED')` tells which build is running. `sys._is_gil_enabled()` tells whether the GIL is active right now. Even on the free-threaded build it can be turned back on, with `PYTHON_GIL=1` / `-X gil=1`, or automatically by importing a C extension that isn't marked as safe without the GIL.

Threads have always helped with I/O-bound work even with the GIL, because blocking I/O calls release it (see `asyncio/04_blocking/01_to_thread`). This example is only about CPU-bound work.
