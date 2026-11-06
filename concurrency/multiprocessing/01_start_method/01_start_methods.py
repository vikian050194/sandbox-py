import multiprocessing as mp
import os
import time

# module level code runs again in every process that re-imports this file
print(f'module imported in pid {os.getpid()} as {__name__}')

config = 'initial'


def child(queue):
    queue.put(f'pid {os.getpid()}, parent {os.getppid()}, config: {config}')


def run(method):
    # a context is the multiprocessing API bound to one start method, without changing the global default
    ctx = mp.get_context(method)
    queue = ctx.Queue()
    start = time.perf_counter()
    process = ctx.Process(target=child, args=(queue,))
    process.start()
    result = queue.get()
    process.join()
    elapsed = time.perf_counter() - start
    return result, elapsed


def main():
    global config
    # changed after import: visible only to children that get a copy of this process memory
    config = 'changed at runtime'
    print(f'main pid {os.getpid()}')
    # since 3.14 the default on Linux is forkserver (it was fork before), macOS and Windows use spawn
    print(f'default start method: {mp.get_start_method()}\n')
    # fork: copies the parent process as is, fast, but unsafe if the parent has threads
    # spawn: starts a fresh interpreter, re-imports the main module, the slowest
    # forkserver: a clean server process is started once, then every child is forked from it,
    # that's why it is run twice: the first run includes starting the server
    for method in ('fork', 'spawn', 'forkserver', 'forkserver'):
        print(f'--- {method} ---')
        result, elapsed = run(method)
        print(f'child: {result}')
        print(f'took {elapsed:.3f}s\n')


# required for spawn and forkserver: the re-imported module must not start processes again
if __name__ == '__main__':
    main()
