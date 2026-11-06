import asyncio
import time


async def worker(name, delay, barrier, fail=False):
    print(f'worker({name}) preparing for {delay}s')
    await asyncio.sleep(delay)
    if fail:
        print(f'worker({name}) failed, aborting barrier')
        # puts the barrier into broken state, all waiting and future wait() calls raise BrokenBarrierError
        await barrier.abort()
        raise ValueError(f'{name} failed')
    print(f'worker({name}) ready, waiting for others ({barrier.n_waiting} already waiting)')
    try:
        # blocks until the number of waiting coroutines reaches barrier.parties,
        # then releases all of them at once and returns a unique index from 0 to parties - 1
        index = await barrier.wait()
    except asyncio.BrokenBarrierError:
        print(f'worker({name}) barrier is broken')
        raise
    print(f'worker({name}) passed the barrier with index {index}')
    return index


async def meet():
    barrier = asyncio.Barrier(3)
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(worker('a', 3, barrier)),
            tg.create_task(worker('b', 1, barrier)),
            tg.create_task(worker('c', 2, barrier)),
        ]
    return [task.result() for task in tasks]


async def broken():
    barrier = asyncio.Barrier(3)
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(worker('a', 3, barrier, fail=True)),
            tg.create_task(worker('b', 1, barrier)),
            tg.create_task(worker('c', 2, barrier)),
        ]
    return [task.result() for task in tasks]


async def main():
    for runner in (meet, broken):
        print(f'--- {runner.__name__} ---')
        start = time.perf_counter()
        try:
            results = await runner()
            print(f'results: {results}')
        except* ValueError as eg:
            print(f'handled ValueError: {eg.exceptions}')
        except* asyncio.BrokenBarrierError as eg:
            print(f'handled BrokenBarrierError: {eg.exceptions}')
        elapsed = time.perf_counter() - start
        print(f'took {elapsed:.2f}s\n')


asyncio.run(main())
