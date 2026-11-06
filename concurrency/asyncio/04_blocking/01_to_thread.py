import asyncio
import threading
import time


async def ticker():
    # shows whether the event loop is alive: it can only tick while nothing blocks the loop
    while True:
        print('tick')
        await asyncio.sleep(0.5)


def blocking_io(name, delay):
    # a regular function that blocks the calling thread, like requests.get or a heavy file operation
    print(f'blocking_io({name}) started in {threading.current_thread().name}')
    time.sleep(delay)
    print(f'blocking_io({name}) finished after {delay}s')
    return f'{name} data'


async def blocking():
    # called directly from a coroutine, it blocks the event loop thread itself,
    # so no other coroutine (ticker included) can run until it returns
    return [blocking_io('a', 2)]


async def to_thread():
    # to_thread runs the function in the loop's default ThreadPoolExecutor and awaits its result,
    # the loop thread stays free and keeps running other coroutines
    return [await asyncio.to_thread(blocking_io, 'a', 2)]


async def to_thread_gather():
    # several blocking calls run in parallel threads, so they take as long as the longest one
    return await asyncio.gather(
        asyncio.to_thread(blocking_io, 'a', 2),
        asyncio.to_thread(blocking_io, 'b', 2),
    )


async def main():
    for runner in (blocking, to_thread, to_thread_gather):
        print(f'--- {runner.__name__} ---')
        start = time.perf_counter()
        ticker_task = asyncio.create_task(ticker())
        # gives the ticker a chance to start before the runner
        await asyncio.sleep(0)
        results = await runner()
        ticker_task.cancel()
        print(f'results: {results}')
        elapsed = time.perf_counter() - start
        print(f'took {elapsed:.2f}s\n')


asyncio.run(main())
