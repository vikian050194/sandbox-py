# 02_pool_comparison

## Output

```
--- sequential ---
results: [17984, 17984, 17984, 17984]
took 1.47s

--- threads ---
results: [17984, 17984, 17984, 17984]
took 1.55s

--- processes ---
results: [17984, 17984, 17984, 17984]
took 0.51s

--- interpreter_threads ---
results: [17984, 17984, 17984, 17984]
took 0.41s
```

## Explanation

The same CPU-bound function runs 4 times, on an 8-core machine and the regular build with a GIL.

- **`threads`**: `ThreadPoolExecutor`. All threads share one GIL, so there's no speedup over sequential.
- **`processes`**: `ProcessPoolExecutor`. Every process has its own interpreter and GIL, so the work runs on 4 cores (~3× faster). The cost: starting processes, more memory, and pickling arguments and results between processes.
- **`interpreter_threads`**: `InterpreterPoolExecutor` (3.14). Every worker is a thread running its own subinterpreter with its own GIL, so the work also runs in parallel, but inside one process. Starting an interpreter is cheaper than starting a process, which is why it's the fastest here. Arguments and results are still pickled, since interpreters don't share objects.

All three executors have the same `concurrent.futures` API, so switching between them is a one-line change. Subinterpreters have limits: some C extensions don't support them yet, and only shareable or picklable data can cross the boundary.
