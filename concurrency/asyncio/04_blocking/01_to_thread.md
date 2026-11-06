# 01_to_thread

## Output

```
--- blocking ---
tick
blocking_io(a) started in MainThread
blocking_io(a) finished after 2s
results: ['a data']
took 2.00s

--- to_thread ---
tick
blocking_io(a) started in asyncio_0
tick
tick
tick
tick
blocking_io(a) finished after 2s
results: ['a data']
took 2.01s

--- to_thread_gather ---
tick
blocking_io(a) started in asyncio_0
blocking_io(b) started in asyncio_1
tick
tick
tick
blocking_io(a) finished after 2s
blocking_io(b) finished after 2s
results: ['a data', 'b data']
took 2.00s
```

## Explanation

- **`ticker`**: a background coroutine that prints every 0.5s. It can only tick while the event loop is free, so it shows whether anything is blocking the loop.
- **`blocking`**: `time.sleep` (or any blocking call like `requests.get` or a slow file operation) called directly from a coroutine runs in the event loop's own thread (`MainThread`). Nothing else can run until it returns: the ticker stops for 2s.
- **`to_thread`**: `asyncio.to_thread` runs the function in a worker thread (`asyncio_0`) from the loop's default `ThreadPoolExecutor` and returns an awaitable. The loop stays free and the ticker keeps ticking. It's a simpler form of `loop.run_in_executor(None, func, *args)`, and it also passes along `contextvars`.
- **`to_thread_gather`**: several blocking calls in different threads run in parallel, so two 2s calls take 2s in total.

This helps with blocking I/O. For CPU-bound pure Python code, threads are limited by the GIL (see `threading/01_free_threading`). `asyncio.run(main(), debug=True)` logs a warning for every step that blocks the loop for longer than 100ms, which helps to find such calls.
