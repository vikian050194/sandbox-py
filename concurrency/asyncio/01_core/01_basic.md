# 01_basic

## Output

```
type: <class 'coroutine'>
greet(World) started
greet(World) finished after 1s
Hello World!
```

## Explanation

- **`async def`**: calling `greet(...)` doesn't run any of its code. It only creates a coroutine object, which is why the type line prints first.
- **`await`**: runs the coroutine and returns its result. `asyncio.sleep` pauses the coroutine and hands control back to the event loop.
- **`asyncio.run(main())`**: the entry point. It creates the event loop, runs `main()` until it finishes, then closes the loop.
