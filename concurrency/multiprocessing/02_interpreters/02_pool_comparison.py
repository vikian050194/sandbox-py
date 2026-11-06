import time
from concurrent.futures import InterpreterPoolExecutor, ProcessPoolExecutor, ThreadPoolExecutor

WORKERS = 4
LIMIT = 200_000


def count_primes(limit):
    # pure Python CPU-bound work
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
    # threads share one GIL (on the regular build), so CPU-bound work doesn't run in parallel
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        return list(executor.map(count_primes, [LIMIT] * WORKERS))


def processes():
    # every process has its own interpreter and GIL, arguments and results are pickled between processes
    with ProcessPoolExecutor(max_workers=WORKERS) as executor:
        return list(executor.map(count_primes, [LIMIT] * WORKERS))


def interpreter_threads():
    # since 3.14: every worker thread runs its own subinterpreter with its own GIL, all in one process;
    # arguments and results are still pickled, since interpreters don't share objects
    with InterpreterPoolExecutor(max_workers=WORKERS) as executor:
        return list(executor.map(count_primes, [LIMIT] * WORKERS))


def main():
    for runner in (sequential, threads, processes, interpreter_threads):
        print(f'--- {runner.__name__} ---')
        start = time.perf_counter()
        results = runner()
        print(f'results: {results}')
        elapsed = time.perf_counter() - start
        print(f'took {elapsed:.2f}s\n')


# processes and subinterpreters both import this script again
if __name__ == '__main__':
    main()
