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


async def stubborn_fetch(name, delay):
    print(f'stubborn_fetch({name}) started')
    try:
        await asyncio.sleep(delay)
    except asyncio.CancelledError:
        task = asyncio.current_task()
        # number of pending cancel() requests for this task
        print(f'stubborn_fetch({name}) cancel requested, cancelling() = {task.cancelling()}')
        # uncancel() decrements that counter, returning 0 means nobody else asked to cancel the task,
        # so it is safe to swallow the cancellation and continue
        if task.uncancel() == 0:
            print(f'stubborn_fetch({name}) ignores cancellation and retries')
            await asyncio.sleep(delay)
        else:
            raise
    print(f'stubborn_fetch({name}) finished')
    return f'{name} data'


async def background():
    # create_task schedules the coroutine to run on the event loop as soon as the current one yields control
    task = asyncio.create_task(fetch('a', 2))
    print(f'task created, done: {task.done()}')
    # while main sleeps, the task is running
    await asyncio.sleep(1)
    print(f'main did other work for 1s, done: {task.done()}')
    # awaiting the task waits for the rest of it and returns its result
    result = await task
    print(f'task awaited, done: {task.done()}')
    return result


async def cancel():
    task = asyncio.create_task(fetch('a', 2))
    await asyncio.sleep(1)
    # cancel() only requests cancellation, CancelledError is thrown into the task at its next await
    task.cancel()
    print(f'cancel requested, done: {task.done()}')
    try:
        await task
    except asyncio.CancelledError:
        print(f'task cancelled: {task.cancelled()}')
    return None


async def uncancel():
    task = asyncio.create_task(stubborn_fetch('a', 1))
    await asyncio.sleep(0.5)
    task.cancel()
    return await task


async def main():
    for runner in (background, cancel, uncancel):
        print(f'--- {runner.__name__} ---')
        start = time.perf_counter()
        results = await runner()
        print(f'results: {results}')
        elapsed = time.perf_counter() - start
        print(f'took {elapsed:.2f}s\n')


asyncio.run(main())
