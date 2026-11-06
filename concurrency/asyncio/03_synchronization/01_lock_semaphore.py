import asyncio
import contextlib
import time


async def increment(name, counter, lock):
    async with lock:
        value = counter['value']
        # an await in the middle of read-modify-write lets other coroutines run and read the same old value
        await asyncio.sleep(0.1)
        counter['value'] = value + 1
        print(f'increment({name}) {value} -> {value + 1}')


async def download(name, semaphore, active):
    async with semaphore:
        active.add(name)
        print(f'download({name}) started, active: {sorted(active)}')
        await asyncio.sleep(1)
        active.remove(name)
        print(f'download({name}) finished')
    return f'{name} data'


async def no_lock():
    counter = {'value': 0}
    # nullcontext does nothing, it only keeps the same async with code for comparison
    lock = contextlib.nullcontext()
    async with asyncio.TaskGroup() as tg:
        for name in 'abcde':
            tg.create_task(increment(name, counter, lock))
    return counter['value']


async def with_lock():
    counter = {'value': 0}
    # only one coroutine at a time can hold the lock, others wait in async with
    lock = asyncio.Lock()
    async with asyncio.TaskGroup() as tg:
        for name in 'abcde':
            tg.create_task(increment(name, counter, lock))
    return counter['value']


async def limited_downloads():
    # semaphore is a lock that can be held by up to N coroutines at the same time
    semaphore = asyncio.Semaphore(2)
    active = set()
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(download(name, semaphore, active)) for name in 'abcdef']
    return [task.result() for task in tasks]


async def main():
    for runner in (no_lock, with_lock, limited_downloads):
        print(f'--- {runner.__name__} ---')
        start = time.perf_counter()
        results = await runner()
        print(f'results: {results}')
        elapsed = time.perf_counter() - start
        print(f'took {elapsed:.2f}s\n')


asyncio.run(main())
