from concurrent import interpreters

counter = 0


def increment():
    # runs inside the interpreter that calls it, so it changes that interpreter's copy of the module
    global counter
    counter += 1
    return counter


def worker(queue, name):
    # objects from the main interpreter can't be shared, only sent through a queue as copies
    for i in range(3):
        queue.put(f'{name}: item {i}')
    queue.put(None)


def isolation():
    # a subinterpreter lives in the same process, but has its own modules, globals and (since 3.12) its own GIL
    interp = interpreters.create()
    try:
        print(f'main counter after increment: {increment()}')
        # call() runs a function in the subinterpreter and returns a copy of its result;
        # the function is pickled by reference, so the subinterpreter imports this script on its own
        # (as '<fake __main__>', that's why the __name__ guard at the bottom is needed)
        print(f'sub counter after increment: {interp.call(increment)}')
        print(f'sub counter after increment: {interp.call(increment)}')
        print(f'main counter is unchanged: {counter}')
    finally:
        interp.close()


def exec_code():
    interp = interpreters.create()
    try:
        # prepare_main puts shareable values into the subinterpreter's __main__ module
        interp.prepare_main(name='sub')
        # exec() runs source code in that __main__, like a separate script;
        # the subinterpreter has its own sys.stdout object, so when output is not a terminal,
        # prints from both interpreters can come out of order
        interp.exec('import sys; print(f"hello from {name}, sys.modules count: {len(sys.modules)}")')
        # errors are not propagated as is, they arrive wrapped into ExecutionFailed
        interp.exec('raise ValueError("oops")')
    except interpreters.ExecutionFailed as e:
        print(f'raised: {type(e).__name__}, original: {e.excinfo.type.__name__}: {e.excinfo.msg}')
    finally:
        interp.close()


def queue_in_thread():
    queue = interpreters.create_queue()
    interp = interpreters.create()
    try:
        # call_in_thread runs the call in a new thread, so the main interpreter can work at the same time
        thread = interp.call_in_thread(worker, queue, 'sub')
        while (item := queue.get()) is not None:
            print(f'main got: {item}')
        thread.join()
    finally:
        interp.close()


def main():
    for runner in (isolation, exec_code, queue_in_thread):
        print(f'--- {runner.__name__} ---')
        runner()
        print()


if __name__ == '__main__':
    main()
