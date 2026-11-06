import asyncio
import contextlib


async def ticks(count, delay):
    # async generator: async def with yield, it can await between the values it produces
    for i in range(count):
        await asyncio.sleep(delay)
        yield i


class Ticks:
    # the same as ticks(), written as a class implementing the async iterator protocol
    def __init__(self, count, delay):
        self.count = count
        self.delay = delay
        self.current = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.current >= self.count:
            # async counterpart of StopIteration
            raise StopAsyncIteration
        await asyncio.sleep(self.delay)
        self.current += 1
        return self.current - 1


class Connection:
    # async context manager protocol: both enter and exit can await, e.g. to open and close a socket
    def __init__(self, name):
        self.name = name

    async def __aenter__(self):
        await asyncio.sleep(0.1)
        print(f'Connection({self.name}) opened')
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await asyncio.sleep(0.1)
        print(f'Connection({self.name}) closed, exception: {exc!r}')
        # returning a truthy value would suppress the exception
        return False

    async def query(self, sql):
        await asyncio.sleep(0.1)
        return f'{self.name}: {sql} -> ok'


@contextlib.asynccontextmanager
async def connection(name):
    # the same as Connection, written as an async generator:
    # code before yield is __aenter__, code after it is __aexit__
    conn = Connection(name)
    await asyncio.sleep(0.1)
    print(f'connection({name}) opened')
    try:
        yield conn
    finally:
        await asyncio.sleep(0.1)
        print(f'connection({name}) closed')


async def async_generator():
    results = []
    async for i in ticks(3, 0.1):
        print(f'got {i}')
        results.append(i)
    return results


async def async_iterator_class():
    results = []
    async for i in Ticks(3, 0.1):
        print(f'got {i}')
        results.append(i)
    return results


async def async_comprehension():
    # comprehensions support async for too, and await in the expression part
    return [i * 10 async for i in ticks(3, 0.1) if i != 1]


async def async_context_manager_class():
    async with Connection('db') as conn:
        return [await conn.query('select 1')]


async def async_context_manager_decorator():
    async with connection('db') as conn:
        return [await conn.query('select 1')]


async def async_context_manager_exception():
    # __aexit__ runs even when the body raises, and receives the exception
    async with Connection('db') as conn:
        await conn.query('select 1')
        raise ValueError('query failed')


async def main():
    for runner in (
        async_generator,
        async_iterator_class,
        async_comprehension,
        async_context_manager_class,
        async_context_manager_decorator,
        async_context_manager_exception,
    ):
        print(f'--- {runner.__name__} ---')
        try:
            results = await runner()
            print(f'results: {results}\n')
        except ValueError as e:
            print(f'raised: {e!r}\n')


asyncio.run(main())
