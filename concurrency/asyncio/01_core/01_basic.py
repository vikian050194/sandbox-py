import asyncio


async def greet(name, delay):
    print(f'greet({name}) started')
    # suspends this coroutine, gives control back to the event loop
    await asyncio.sleep(delay)
    print(f'greet({name}) finished after {delay}s')
    return f'Hello {name}!'


async def main():
    # calling an async function does not run it, it only creates a coroutine object
    coroutine = greet('World', 1)
    print(f'type: {type(coroutine)}')

    # await runs the coroutine and gives back its return value
    result = await coroutine
    print(result)


# asyncio.run creates an event loop, runs main() until it completes and closes the loop
asyncio.run(main())
