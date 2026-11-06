import asyncio
import time


async def produce(queue, items):
    for item in items:
        # with maxsize set, put() waits while the queue is full, so a fast producer can't run far ahead
        await queue.put(item)
        print(f'produce put {item}, size: {queue.qsize()}')
    print('produce done')


async def consume_until_sentinel(name, queue):
    processed = []
    while True:
        item = await queue.get()
        if item is None:
            print(f'consume({name}) got sentinel, stopping')
            return processed
        # simulates slow processing
        await asyncio.sleep(0.5)
        print(f'consume({name}) processed {item}')
        processed.append(item)


async def consume_until_shutdown(name, queue):
    processed = []
    while True:
        try:
            item = await queue.get()
        # get() raises QueueShutDown only after the queue is shut down and all items are taken
        except asyncio.QueueShutDown:
            print(f'consume({name}) queue is shut down, stopping')
            return processed
        await asyncio.sleep(0.5)
        print(f'consume({name}) processed {item}')
        processed.append(item)


async def sentinel():
    queue = asyncio.Queue(maxsize=2)
    async with asyncio.TaskGroup() as tg:
        consumers = [tg.create_task(consume_until_sentinel(name, queue)) for name in 'ab']
        await produce(queue, range(6))
        # old way: one special value per consumer, the producer has to know how many consumers there are
        for _ in consumers:
            await queue.put(None)
    return [task.result() for task in consumers]


async def shutdown():
    queue = asyncio.Queue(maxsize=2)
    async with asyncio.TaskGroup() as tg:
        consumers = [tg.create_task(consume_until_shutdown(name, queue)) for name in 'ab']
        await produce(queue, range(6))
        # since 3.13: no more put() is allowed, consumers take what is left and then get QueueShutDown;
        # shutdown(immediate=True) would also drop the remaining items
        queue.shutdown()
    return [task.result() for task in consumers]


async def main():
    for runner in (sentinel, shutdown):
        print(f'--- {runner.__name__} ---')
        start = time.perf_counter()
        results = await runner()
        print(f'results: {results}')
        elapsed = time.perf_counter() - start
        print(f'took {elapsed:.2f}s\n')


asyncio.run(main())
