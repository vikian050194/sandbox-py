import sys
import sysconfig
import time
from concurrent.futures import ThreadPoolExecutor

WORKERS = 4
LIMIT = 200_000


def count_primes(limit):
    # pure Python CPU-bound work, it never waits for I/O, so it never releases the GIL voluntarily
    count = 0
    for n in range(2, limit):
        for d in range(2, int(n ** 0.5) + 1):
            if n % d == 0:
                break
        else:
            count += 1
    return count


def sequential():
    return [count_primes(LIMIT) for _ in range(WORKERS)]


def threads():
    # with the GIL only one thread executes Python bytecode at a time, so threads take turns
    # and the total time is about the same as sequential; without the GIL they run on separate cores
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        return list(executor.map(count_primes, [LIMIT] * WORKERS))


def main():
    # Py_GIL_DISABLED is 1 for the free-threaded build (python3.14t),
    # but even there the GIL can be turned back on, e.g. with PYTHON_GIL=1 or by an incompatible C extension
    print(f'free-threaded build: {bool(sysconfig.get_config_var("Py_GIL_DISABLED"))}')
    print(f'GIL enabled: {sys._is_gil_enabled()}\n')
    for runner in (sequential, threads):
        print(f'--- {runner.__name__} ---')
        start = time.perf_counter()
        results = runner()
        print(f'results: {results}')
        elapsed = time.perf_counter() - start
        print(f'took {elapsed:.2f}s\n')


main()
