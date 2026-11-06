# 03_introspection

## Output

```
* Task(name='worker-a', id=0x7fe8bda68410)
  + Call stack:
  |   File '/home/kirill/.pyenv/versions/3.14.2/lib/python3.14/asyncio/graph.py', line 276, in print_call_graph()
  |   File '/home/kirill/git/sandbox/py/concurrency/asyncio/06_advanced/03_introspection.py', line 15, in async query()
  |   File '/home/kirill/git/sandbox/py/concurrency/asyncio/06_advanced/03_introspection.py', line 21, in async fetch()
  |   File '/home/kirill/git/sandbox/py/concurrency/asyncio/06_advanced/03_introspection.py', line 25, in async worker()
  + Awaited by:
    * Task(name='Task-1', id=0x7fe8bda68230)
      + Call stack:
      |   File '/home/kirill/.pyenv/versions/3.14.2/lib/python3.14/asyncio/tasks.py', line 702, in async sleep()
      |   File '/home/kirill/git/sandbox/py/concurrency/asyncio/06_advanced/03_introspection.py', line 43, in async main()

task: worker-b
  call stack (innermost first): ['sleep', 'query', 'fetch', 'worker']
  awaited by: ['Task-1']

results: ['a data', 'b data']
```

With `--wait`, inspected from outside:

```
$ python -m asyncio ps PID
tid        task id              task name            coroutine stack                                    awaiter chain                                      awaiter name    awaiter id
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
66051      0x7f41ac990230       Task-1               TaskGroup._aexit -> TaskGroup.__aexit__ -> main                                                                       0x0
66051      0x7f41ac990410       worker-a             sleep -> query -> fetch -> worker                  TaskGroup._aexit -> TaskGroup.__aexit__ -> main    Task-1          0x7f41ac990230
66051      0x7f41ac9743f0       worker-b             sleep -> query -> fetch -> worker                  TaskGroup._aexit -> TaskGroup.__aexit__ -> main    Task-1          0x7f41ac990230

$ python -m asyncio pstree PID
└── (T) Task-1
    └──  main /home/kirill/git/sandbox/py/concurrency/asyncio/06_advanced/03_introspection.py:40
        └──  TaskGroup.__aexit__ /home/kirill/.pyenv/versions/3.14.2/lib/python3.14/asyncio/taskgroups.py:72
            └──  TaskGroup._aexit /home/kirill/.pyenv/versions/3.14.2/lib/python3.14/asyncio/taskgroups.py:121
                ├── (T) worker-a
                │   └──  worker /home/kirill/git/sandbox/py/concurrency/asyncio/06_advanced/03_introspection.py:25
                │       └──  fetch /home/kirill/git/sandbox/py/concurrency/asyncio/06_advanced/03_introspection.py:21
                │           └──  query /home/kirill/git/sandbox/py/concurrency/asyncio/06_advanced/03_introspection.py:16
                │               └──  sleep /home/kirill/.pyenv/versions/3.14.2/lib/python3.14/asyncio/tasks.py:702
                └── (T) worker-b
                    └──  worker /home/kirill/git/sandbox/py/concurrency/asyncio/06_advanced/03_introspection.py:25
                        └──  fetch /home/kirill/git/sandbox/py/concurrency/asyncio/06_advanced/03_introspection.py:21
                            └──  query /home/kirill/git/sandbox/py/concurrency/asyncio/06_advanced/03_introspection.py:16
                                └──  sleep /home/kirill/.pyenv/versions/3.14.2/lib/python3.14/asyncio/tasks.py:702
```

## Explanation

- **Why it's needed**: a regular traceback shows only the current task's frames. With tasks, the interesting part is often who awaits whom across tasks, e.g. which task is stuck and what is waiting for it.
- **`asyncio.print_call_graph()`** (3.14): called inside `worker-a`, it prints that task's coroutine chain (`worker -> fetch -> query`), and then the tasks awaiting it. Here that's `Task-1` (the main task, waiting in the `TaskGroup`).
- **`asyncio.capture_call_graph(task)`** (3.14): the same information as data. `call_stack` has frame entries, innermost first, and `awaited_by` has graphs of the awaiting tasks. It works for any task, not only the current one. `asyncio.format_call_graph()` returns the printed form as a string.
- **`python -m asyncio ps PID` / `pstree PID`** (3.14): the same view of a running process from outside, without changing its code. `ps` shows a table of tasks; `pstree` shows the tree from the main task down to every leaf. This helps to find where a production process hangs.

The external tools read another process's memory, so they need ptrace permission. On this machine `/proc/sys/kernel/yama/ptrace_scope` is `1`, which allows that only for a parent process, so running them from another terminal needs `sudo`. The output above was captured by a script that started the example as its child and called the same functions from `asyncio.tools`.
