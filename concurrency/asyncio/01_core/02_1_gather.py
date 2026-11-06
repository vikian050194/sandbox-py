import asyncio
import time


async def fetch(name, delay):
    print(f'fetch({name}) started')
    # simulates waiting for I/O (network, disk, etc.)
    await asyncio.sleep(delay)
    print(f'fetch({name}) finished after {delay}s')
    return f'{name} data'


async def sequential():
    # each await blocks main flow until that coroutine completes, so delays add up: 1 + 2 + 3
    results = []
    for name, delay in [('a', 1), ('b', 2), ('c', 3)]:
        results.append(await fetch(name, delay))
    return results


async def concurrent():
    # gather wraps every coroutine into a task and schedules them all at once,
    # so they wait in parallel and total time is the longest delay: max(1, 2, 3)
    # results come back in the order of arguments, not in the order of completion
    return await asyncio.gather(
        fetch('a', 3),
        fetch('b', 1),
        fetch('c', 2),
    )


async def main():
    for runner in (sequential, concurrent):
        print(f'--- {runner.__name__} ---')
        start = time.perf_counter()
        results = await runner()
        elapsed = time.perf_counter() - start
        print(f'results: {results}')
        print(f'took {elapsed:.2f}s\n')


asyncio.run(main())
