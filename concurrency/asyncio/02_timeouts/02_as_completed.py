import asyncio
import time


async def fetch(name, delay):
    print(f'fetch({name}) started')
    try:
        # simulates waiting for I/O (network, disk, etc.)
        await asyncio.sleep(delay)
    except asyncio.CancelledError:
        print(f'fetch({name}) cancelled')
        raise
    print(f'fetch({name}) finished after {delay}s')
    return f'{name} data'


async def plain_iterator():
    tasks = [
        asyncio.create_task(fetch('a', 3), name='a'),
        asyncio.create_task(fetch('b', 1), name='b'),
        asyncio.create_task(fetch('c', 2), name='c'),
    ]
    results = []
    # classic form: yields new awaitables in order of completion, not the original tasks,
    # so it's not possible to tell which task finished other than from its result
    for next_done in asyncio.as_completed(tasks):
        result = await next_done
        print(f'got: {result}, is original task: {next_done in tasks}')
        results.append(result)
    return results


async def async_iterator():
    results = []
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(fetch('a', 3), name='a'),
            tg.create_task(fetch('b', 1), name='b'),
            tg.create_task(fetch('c', 2), name='c'),
        ]
        # since 3.13 async for yields the original tasks, already done, as they complete
        async for task in asyncio.as_completed(tasks):
            print(f'got: {task.get_name()} -> {task.result()}, is original task: {task in tasks}')
            results.append(task.result())
    return results


async def with_timeout():
    results = []
    # TaskGroup cancels the tasks left running when the timeout error leaves the block,
    # and wraps that error into ExceptionGroup like any other error from the block
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(fetch('a', 3), name='a'),
            tg.create_task(fetch('b', 1), name='b'),
            tg.create_task(fetch('c', 2), name='c'),
        ]
        # the timeout covers the whole iteration, TimeoutError is raised when it expires
        async for task in asyncio.as_completed(tasks, timeout=2.5):
            print(f'got: {task.get_name()} -> {task.result()}')
            results.append(task.result())
    return results


async def main():
    for runner in (plain_iterator, async_iterator, with_timeout):
        print(f'--- {runner.__name__} ---')
        start = time.perf_counter()
        try:
            results = await runner()
            print(f'results: {results}')
        except* TimeoutError as eg:
            print(f'raised: {eg!r}')
        elapsed = time.perf_counter() - start
        print(f'took {elapsed:.2f}s\n')


asyncio.run(main())
