# 01_interpreters

## Output

```
--- isolation ---
main counter after increment: 1
sub counter after increment: 1
sub counter after increment: 2
main counter is unchanged: 1

--- exec_code ---
hello from sub, sys.modules count: 53
raised: ExecutionFailed, original: ValueError: oops

--- queue_in_thread ---
main got: sub: item 0
main got: sub: item 1
main got: sub: item 2
```

## Explanation

- **What a subinterpreter is**: another Python interpreter inside the same process. It has its own modules, globals and, since 3.12, its own GIL. `concurrent.interpreters` (3.14, PEP 734) is the first public Python API for it.
- **`isolation`**: `interp.call(increment)` runs the function inside the subinterpreter and returns a copy of the result. The subinterpreter has its own copy of the module, so its `counter` goes 1, 2 while the main one stays 1. The function is passed by reference, so the subinterpreter imports this script itself (as `<fake __main__>`), and the `__name__` guard is needed just like with `spawn`.
- **`exec_code`**: `prepare_main(name=...)` puts values into the subinterpreter's `__main__`, and `exec(code)` runs source code there like a separate script. Exceptions don't cross the boundary as they are: they arrive as `ExecutionFailed`, with the original type and message in `excinfo`.
- **`queue_in_thread`**: interpreters can't share regular objects. `interpreters.create_queue()` passes copies of values between them. `call_in_thread` runs the call in a new thread, so the main interpreter reads the queue at the same time.

Each interpreter has its own `sys.stdout` object. With output redirected (not a terminal), prints from the two can come out of order; the output above was captured with `PYTHONUNBUFFERED=1`.
