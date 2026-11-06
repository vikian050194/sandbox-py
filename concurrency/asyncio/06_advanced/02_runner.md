# 02_runner

## Output

```
--- with_asyncio_run ---
heartbeat(a) beat
heartbeat(a) cancelled
after the first run, task cancelled: True
second run used the same loop: False

--- with_runner ---
heartbeat(a) beat
after the first run, task cancelled: False
heartbeat(a) beat
second run used the same loop: True
runner.get_loop() is that loop: True
heartbeat(a) cancelled
after the with block, task cancelled: True
```

## Explanation

- **`with_asyncio_run`**: every `asyncio.run` creates a new event loop and closes it at the end, cancelling all tasks left on it. The heartbeat task started in the first run is cancelled as soon as that run ends, and the second run gets a different loop.
- **`with_runner`** (3.11+): `asyncio.Runner` keeps one loop for several `runner.run(...)` calls. The heartbeat task survives the first run. Between runs it's paused, because nothing is running the loop, and it continues during the second run. `runner.get_loop()` gives direct access to that loop.
- **Closing**: when the `with` block ends, `Runner` cancels remaining tasks and closes the loop, just like `asyncio.run`.

`main()` is a regular function here. `Runner` is for synchronous code that needs to enter async code several times while sharing state bound to one loop, e.g. tests, or a sync app calling an async library. It also accepts `debug=` and `loop_factory=`, e.g. to use `uvloop`.
