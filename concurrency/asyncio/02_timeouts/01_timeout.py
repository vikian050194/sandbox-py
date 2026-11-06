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


async def block_in_time():
    # the deadline applies to the whole block, not to each await inside it
    async with asyncio.timeout(3):
        a = await fetch('a', 1)
        b = await fetch('b', 1)
    return [a, b]


async def block_expired():
    # when the deadline passes, the current await is cancelled
    # and the CancelledError is converted to TimeoutError on exit from the block
    async with asyncio.timeout(3) as cm:
        try:
            a = await fetch('a', 2)
            b = await fetch('b', 2)
        finally:
            print(f'deadline expired: {cm.expired()}')
    return [a, b]


async def reschedule():
    # deadline can be unknown at the start (None) and set or moved later, it is an absolute loop time
    async with asyncio.timeout(None) as cm:
        cm.reschedule(asyncio.get_running_loop().time() + 1)
        print('deadline set to 1s from now')
        a = await fetch('a', 2)
    return [a]


async def wait_for_expired():
    # older API: the timeout wraps a single awaitable, which is cancelled on expiration
    a = await asyncio.wait_for(fetch('a', 3), timeout=2)
    return [a]


async def main():
    for runner in (block_in_time, block_expired, reschedule, wait_for_expired):
        print(f'--- {runner.__name__} ---')
        start = time.perf_counter()
        try:
            results = await runner()
            print(f'results: {results}')
        # since 3.11 asyncio.TimeoutError is just an alias of the built-in TimeoutError
        except TimeoutError as e:
            print(f'raised: {e!r}')
        elapsed = time.perf_counter() - start
        print(f'took {elapsed:.2f}s\n')


asyncio.run(main())
