import asyncio

cache = {'a': 'a data (cached)'}


async def fetch(name):
    print(f'fetch({name}) started')
    # a cache hit returns without any await, so the coroutine completes in one step
    if name in cache:
        print(f'fetch({name}) cache hit')
        return cache[name]
    await asyncio.sleep(0.1)
    print(f'fetch({name}) finished')
    return f'{name} data'


async def create(**kwargs):
    tasks = []
    for name in 'ab':
        print(f'creating task {name}')
        task = asyncio.create_task(fetch(name), **kwargs)
        print(f'task {name} created, done: {task.done()}')
        tasks.append(task)
    return [await task for task in tasks]


async def lazy():
    # default: create_task only schedules the coroutine, it starts later, when the current coroutine awaits
    return await create(eager_start=False)


async def eager_start():
    # since 3.14: the coroutine starts running synchronously inside create_task, until its first await;
    # if it finishes without awaiting, the task is done right away and never gets scheduled on the loop
    return await create(eager_start=True)


async def eager_factory():
    # since 3.12: makes every new task on this loop eager;
    # eager_start must not be passed at all here, even eager_start=None would override the factory's default
    asyncio.get_running_loop().set_task_factory(asyncio.eager_task_factory)
    try:
        return await create()
    finally:
        asyncio.get_running_loop().set_task_factory(None)


async def main():
    for runner in (lazy, eager_start, eager_factory):
        print(f'--- {runner.__name__} ---')
        results = await runner()
        print(f'results: {results}\n')


asyncio.run(main())
