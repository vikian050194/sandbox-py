import asyncio
import time


async def handle(reader, writer):
    # called by the server as a new task for every accepted connection
    peer = writer.get_extra_info('peername')
    print(f'server: {peer} connected')
    # reader is an async iterator over lines, it ends when the client closes its side
    async for line in reader:
        message = line.decode().strip()
        print(f'server: {peer} sent {message!r}')
        # simulates slow processing, connections are still served concurrently
        await asyncio.sleep(0.5)
        # write() only puts the data into a buffer, drain() waits until it's flushed enough
        writer.write(message.upper().encode() + b'\n')
        await writer.drain()
    print(f'server: {peer} disconnected')
    writer.close()
    await writer.wait_closed()


async def client(name, port, messages):
    reader, writer = await asyncio.open_connection('127.0.0.1', port)
    replies = []
    for message in messages:
        writer.write(f'{name} {message}\n'.encode())
        await writer.drain()
        reply = await reader.readline()
        print(f'client({name}): got {reply.decode().strip()!r}')
        replies.append(reply.decode().strip())
    writer.close()
    await writer.wait_closed()
    return replies


async def main():
    # port 0 lets the OS pick a free port
    server = await asyncio.start_server(handle, '127.0.0.1', 0)
    port = server.sockets[0].getsockname()[1]
    print(f'server: listening on port {port}\n')
    start = time.perf_counter()
    # closes the server on exit from the block, no new connections are accepted after that
    async with server:
        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(client('a', port, ['hello', 'bye'])),
                tg.create_task(client('b', port, ['hi', 'see you'])),
            ]
    print(f'\nresults: {[task.result() for task in tasks]}')
    elapsed = time.perf_counter() - start
    print(f'took {elapsed:.2f}s')


asyncio.run(main())
