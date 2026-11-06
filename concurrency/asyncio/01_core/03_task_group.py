import asyncio
import time


async def fetch(name, delay, fail=False):
    print(f'fetch({name}) started')
    try:
        # simulates waiting for I/O (network, disk, etc.)
        await asyncio.sleep(delay)
    except asyncio.CancelledError:
        # cancellation is delivered as an exception at the await point where the coroutine is suspended
        print(f'fetch({name}) cancelled')
        # must be re-raised, otherwise the task is not marked as cancelled
        raise
    if fail:
        print(f'fetch({name}) failed after {delay}s')
        raise ValueError(f'{name} failed')
    print(f'fetch({name}) finished after {delay}s')
    return f'{name} data'


async def success():
    # create_task schedules a task right away, exiting the async with block waits for all of them
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(fetch('a', 3)),
            tg.create_task(fetch('b', 1)),
            tg.create_task(fetch('c', 2)),
        ]
    # all tasks are done here, so result() returns immediately
    return [task.result() for task in tasks]


async def failure():
    # the first failure cancels all other tasks of the group, so nothing keeps running in the background
    # (unlike gather in 02_2), then the block waits for cancellation to complete and raises ExceptionGroup
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(fetch('a', 3)),
            tg.create_task(fetch('b', 1, fail=True)),
            tg.create_task(fetch('c', 2)),
        ]
    return [task.result() for task in tasks]


async def main():
    for runner in (success, failure):
        print(f'--- {runner.__name__} ---')
        start = time.perf_counter()
        try:
            results = await runner()
            print(f'results: {results}')
        except ExceptionGroup as eg:
            # errors of all failed tasks are wrapped into a single ExceptionGroup
            print(f'raised: {eg!r}')
        elapsed = time.perf_counter() - start
        print(f'took {elapsed:.2f}s\n')


asyncio.run(main())
