# 01_async_iteration

## Output

```
--- async_generator ---
got 0
got 1
got 2
results: [0, 1, 2]

--- async_iterator_class ---
got 0
got 1
got 2
results: [0, 1, 2]

--- async_comprehension ---
results: [0, 20]

--- async_context_manager_class ---
Connection(db) opened
Connection(db) closed, exception: None
results: ['db: select 1 -> ok']

--- async_context_manager_decorator ---
connection(db) opened
connection(db) closed
results: ['db: select 1 -> ok']

--- async_context_manager_exception ---
Connection(db) opened
Connection(db) closed, exception: ValueError('query failed')
raised: ValueError('query failed')
```

## Explanation

- **`async_generator`**: an `async def` with `yield` is an async generator. It can `await` between values, e.g. to read the next page from the network. It's consumed with `async for`.
- **`async_iterator_class`**: the same iterator written as a class. `__aiter__` returns the iterator, and `async def __anext__` returns the next value or raises `StopAsyncIteration` (the async counterpart of `StopIteration`).
- **`async_comprehension`**: comprehensions accept `async for` (and `await` in the expression), including filtering with `if`.
- **`async_context_manager_class`**: `async def __aenter__` / `__aexit__` let both entering and leaving `async with` await, e.g. to open and close a connection.
- **`async_context_manager_decorator`**: `@contextlib.asynccontextmanager` builds the same thing from an async generator. Code before `yield` is the enter part, code after it is the exit part. `try/finally` around `yield` makes sure the exit part also runs on errors.
- **`async_context_manager_exception`**: when the body raises, `__aexit__` still runs and receives the exception. Returning `False` lets the exception continue, and returning a truthy value would suppress it.
