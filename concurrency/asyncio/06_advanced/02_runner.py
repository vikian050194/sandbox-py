import asyncio


async def heartbeat(name):
    try:
        while True:
            print(f'heartbeat({name}) beat')
            await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        print(f'heartbeat({name}) cancelled')
        raise


async def start_heartbeat(name):
    # returns a task that outlives this coroutine and keeps running on the loop
    return asyncio.create_task(heartbeat(name))


async def work(seconds):
    await asyncio.sleep(seconds)
    return asyncio.get_running_loop()


def with_asyncio_run():
    # every asyncio.run creates a new loop and closes it at the end, cancelling all tasks left on it
    task = asyncio.run(start_heartbeat('a'))
    print(f'after the first run, task cancelled: {task.cancelled()}')
    loop = asyncio.run(work(1))
    print(f'second run used the same loop: {loop is task.get_loop()}')


def with_runner():
    # Runner keeps one loop for several run() calls, it is closed together with the with block
    with asyncio.Runner() as runner:
        task = runner.run(start_heartbeat('a'))
        print(f'after the first run, task cancelled: {task.cancelled()}')
        # the task was paused between run() calls, because nothing was running the loop, and continues now
        loop = runner.run(work(1))
        print(f'second run used the same loop: {loop is task.get_loop()}')
        # the loop is also reachable directly
        print(f'runner.get_loop() is that loop: {runner.get_loop() is loop}')
    # at close, Runner cancels remaining tasks just like asyncio.run does
    print(f'after the with block, task cancelled: {task.cancelled()}')


def main():
    # main is a regular function here: Runner is for code that needs to enter async code several times
    for runner in (with_asyncio_run, with_runner):
        print(f'--- {runner.__name__} ---')
        runner()
        print()


main()
