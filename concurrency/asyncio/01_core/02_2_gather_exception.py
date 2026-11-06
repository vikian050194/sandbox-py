import asyncio
import time


async def fetch(name, delay, fail=False):
    print(f'fetch({name}) started')
    # simulates waiting for I/O (network, disk, etc.)
    await asyncio.sleep(delay)
    if fail:
        print(f'fetch({name}) failed after {delay}s')
        raise ValueError(f'{name} failed')
    print(f'fetch({name}) finished after {delay}s')
    return f'{name} data'


async def propagate():
    # default return_exceptions=False: the first exception is raised to the awaiting caller right away,
    # but the other coroutines are NOT cancelled, they keep running in the background
    return await asyncio.gather(
        fetch('a', 3),
        fetch('b', 1, fail=True),
        fetch('c', 2),
    )


async def collect():
    # return_exceptions=True: exceptions are treated like successful results,
    # gather waits for all coroutines and puts the exception object on the failed one's position
    return await asyncio.gather(
        fetch('a', 3),
        fetch('b', 1, fail=True),
        fetch('c', 2),
        return_exceptions=True,
    )


async def main():
    for runner in (propagate, collect):
        print(f'--- {runner.__name__} ---')
        start = time.perf_counter()
        try:
            results = await runner()
            print(f'results: {results}')
        except ValueError as e:
            print(f'raised: {e!r}')
        elapsed = time.perf_counter() - start
        print(f'took {elapsed:.2f}s\n')
        if runner is propagate:
            # a and c are still running, wait for them so their output doesn't mix with the next runner
            await asyncio.sleep(3)


asyncio.run(main())
