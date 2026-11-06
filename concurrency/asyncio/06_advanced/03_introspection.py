import asyncio
import os
import sys

# run with --wait to keep the program alive and inspect it from another terminal:
# python -m asyncio ps <PID>
# python -m asyncio pstree <PID>
WAIT = '--wait' in sys.argv


async def query(name, delay):
    if name == 'a' and not WAIT:
        # since 3.14: prints the chain of awaits of the current task,
        # including the tasks that await it (TaskGroup's parent task here)
        asyncio.print_call_graph()
    await asyncio.sleep(delay)
    return f'{name} data'


async def fetch(name, delay):
    return await query(name, delay)


async def worker(name, delay):
    return await fetch(name, delay)


async def inspect_task(task):
    # capture_call_graph returns the same information as a structure instead of text
    graph = asyncio.capture_call_graph(task)
    print(f'task: {graph.future.get_name()}')
    print(f'  call stack (innermost first): {[entry.frame.f_code.co_name for entry in graph.call_stack]}')
    print(f'  awaited by: {[parent.future.get_name() for parent in graph.awaited_by]}')


async def main():
    delay = 60 if WAIT else 1
    if WAIT:
        print(f'PID: {os.getpid()}, waiting for {delay}s')
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(worker(name, delay), name=f'worker-{name}') for name in 'ab']
        # gives workers a chance to start and get suspended in asyncio.sleep
        await asyncio.sleep(0.1)
        print()
        await inspect_task(tasks[1])
    print(f'\nresults: {[task.result() for task in tasks]}')


asyncio.run(main())
