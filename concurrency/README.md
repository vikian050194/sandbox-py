# Concurrency

Examples for refreshing Python concurrency knowledge. Target version is Python 3.14.

Structure: `<module>/NN_<group>/NN_<name>.py`, where each group of ideas has its own directory; the numbers give the reading order.

## asyncio

### 01_core

- [x] `01_basic.py` - `async def`, `await`, `asyncio.run`; calling an async function only creates a coroutine object
- [x] `02_1_gather.py` - sequential awaits vs `asyncio.gather`, with timings; results keep the order of arguments
- [x] `02_2_gather_exception.py` - `gather` with a failing coroutine: default `return_exceptions=False` raises the first exception immediately while the others keep running; `return_exceptions=True` waits for all and returns the exception as a result
- [x] `03_task_group.py` - `async with asyncio.TaskGroup()` (3.11+), structured concurrency, the modern alternative to `gather`; a failure in one task cancels the others
- [x] `04_exception_group.py` - `ExceptionGroup` and `except*` (3.11+), needed to handle failures from a TaskGroup
- [x] `05_tasks.py` - `create_task`, `task.cancel()`, handling `CancelledError`, `Task.uncancel()`

### 02_timeouts

- [x] `01_timeout.py` - `async with asyncio.timeout(...)` (3.11+) vs older `wait_for`
- [x] `02_as_completed.py` - `async for t in asyncio.as_completed(...)` (3.13+), yields the original tasks

### 03_synchronization

- [x] `01_lock_semaphore.py` - `asyncio.Lock`, `asyncio.Semaphore` to limit the number of simultaneous "downloads"
- [x] `02_barrier.py` - `asyncio.Barrier` (3.11+), N coroutines wait until all of them reach a point
- [x] `03_queue.py` - producer/consumer with `asyncio.Queue`; `Queue.shutdown()` (3.13+) to stop consumers without sentinel values

### 04_blocking

- [x] `01_to_thread.py` - why `time.sleep` inside a coroutine freezes the event loop, fixed with `asyncio.to_thread` (simpler than `run_in_executor`)

### 05_language

- [x] `01_async_iteration.py` - async generators, `async for`, `async with`, `contextlib.asynccontextmanager`

### 06_advanced

- [x] `01_eager_tasks.py` - `asyncio.eager_task_factory` (3.12+), `eager_start=` in `create_task` (3.14), how it changes execution order
- [x] `02_runner.py` - `asyncio.Runner` (3.11+), several top-level coroutines on the same loop
- [x] `03_introspection.py` - `asyncio.print_call_graph()` / `capture_call_graph()` (3.14); from outside: `python -m asyncio ps <PID>` and `python -m asyncio pstree <PID>`
- [x] `04_tcp_echo.py` - real I/O, TCP echo server and client with `asyncio.start_server`

## threading

### 01_free_threading

- [x] `01_cpu_bound.py` - the same CPU-bound work sequentially and in threads, on the regular build and on the free-threaded build (`python3.14t`, no GIL, officially supported in 3.14); `sys._is_gil_enabled()`

## multiprocessing

### 01_start_method

- [x] `01_start_methods.py` - `fork`, `spawn`, `forkserver` compared: speed, what the child sees, re-import of the main module; default on Linux changed from `fork` to `forkserver` in 3.14

### 02_interpreters

- [x] `01_interpreters.py` - `concurrent.interpreters` (3.14): subinterpreters in one process, isolation, `call`, `exec`, `ExecutionFailed`, queues, `call_in_thread`
- [x] `02_pool_comparison.py` - the same CPU-bound work with `ThreadPoolExecutor`, `ProcessPoolExecutor` and `InterpreterPoolExecutor` (3.14)
