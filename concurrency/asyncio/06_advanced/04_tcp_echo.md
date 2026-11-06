# 04_tcp_echo

## Output

```
server: listening on port 42731

server: ('127.0.0.1', 55730) connected
server: ('127.0.0.1', 55738) connected
server: ('127.0.0.1', 55730) sent 'a hello'
server: ('127.0.0.1', 55738) sent 'b hi'
client(a): got 'A HELLO'
client(b): got 'B HI'
server: ('127.0.0.1', 55730) sent 'a bye'
server: ('127.0.0.1', 55738) sent 'b see you'
client(a): got 'A BYE'
client(b): got 'B SEE YOU'
server: ('127.0.0.1', 55730) disconnected
server: ('127.0.0.1', 55738) disconnected

results: [['A HELLO', 'A BYE'], ['B HI', 'B SEE YOU']]
took 1.03s
```

## Explanation

- **Server**: `asyncio.start_server(handle, host, port)` listens for connections and runs `handle(reader, writer)` as a new task for each one. Port `0` lets the OS pick a free port. `async with server` closes it when the block ends.
- **Streams**: `StreamReader` is an async iterator over lines, so `async for line in reader` runs until the other side closes the connection. `writer.write()` only puts data into a buffer, and `await writer.drain()` waits until the buffer is flushed enough. This gives backpressure against a slow peer.
- **Clients**: `asyncio.open_connection(host, port)` returns the same reader/writer pair. Closing is `writer.close()` followed by `await writer.wait_closed()`.
- **Concurrency**: the server handles every message for 0.5s. Two clients with two messages each would take 2s if served one by one, but the connections are served concurrently, so it takes about 1s, all in one thread.

This is the real use case for asyncio: many network connections that mostly wait for I/O, served by one thread without a thread per connection.
