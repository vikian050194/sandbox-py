import asyncio
import time


async def fetch(name, delay, error=None):
    print(f'fetch({name}) started')
    try:
        # simulates waiting for I/O (network, disk, etc.)
        await asyncio.sleep(delay)
    except asyncio.CancelledError:
        print(f'fetch({name}) cancelled')
        raise
    if error:
        print(f'fetch({name}) failed after {delay}s with {error.__name__}')
        raise error(f'{name} failed')
    print(f'fetch({name}) finished after {delay}s')
    return f'{name} data'


async def one_type():
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(fetch('a', 3)),
            tg.create_task(fetch('b', 1, ValueError)),
            tg.create_task(fetch('c', 2)),
        ]
    return [task.result() for task in tasks]


async def two_types():
    # b and c fail at the same moment, both get to raise before the group starts cancelling,
    # so the ExceptionGroup contains two errors of different types
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(fetch('a', 3)),
            tg.create_task(fetch('b', 1, ValueError)),
            tg.create_task(fetch('c', 1, TypeError)),
        ]
    return [task.result() for task in tasks]


async def unexpected_type():
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(fetch('a', 3)),
            tg.create_task(fetch('b', 1, KeyError)),
            tg.create_task(fetch('c', 2)),
        ]
    return [task.result() for task in tasks]


async def main():
    for runner in (one_type, two_types, unexpected_type):
        print(f'--- {runner.__name__} ---')
        start = time.perf_counter()
        try:
            results = await runner()
            print(f'results: {results}')
        # unlike except, every matching except* clause runs, not only the first one;
        # each clause receives an ExceptionGroup with only the errors of its type
        except* ValueError as eg:
            print(f'handled ValueError: {eg.exceptions}')
        except* TypeError as eg:
            print(f'handled TypeError: {eg.exceptions}')
        # catches whatever is left unmatched by the clauses above,
        # without it the rest would be re-raised as an ExceptionGroup
        except* Exception as eg:
            print(f'handled other: {eg.exceptions}')
        elapsed = time.perf_counter() - start
        print(f'took {elapsed:.2f}s\n')


asyncio.run(main())
