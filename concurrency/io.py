import asyncio


async def worker():
    print("Starting worker")
    await asyncio.sleep(1)
    print("Worker finished")

async def main():
    tasks = []
    for i in range(5):
        tasks.append(asyncio.create_task(worker()))
    await asyncio.gather(*tasks)

asyncio.run(main())