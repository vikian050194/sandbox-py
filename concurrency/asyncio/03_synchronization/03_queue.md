# 03_queue

## Output

```
--- sentinel ---
produce put 0, size: 1
produce put 1, size: 2
produce put 2, size: 1
produce put 3, size: 2
consume(a) processed 0
consume(b) processed 1
produce put 4, size: 1
produce put 5, size: 2
produce done
consume(a) processed 2
consume(b) processed 3
consume(a) processed 4
consume(a) got sentinel, stopping
consume(b) processed 5
consume(b) got sentinel, stopping
results: [[0, 2, 4], [1, 3, 5]]
took 1.50s

--- shutdown ---
produce put 0, size: 1
produce put 1, size: 2
produce put 2, size: 1
produce put 3, size: 2
consume(a) processed 0
consume(b) processed 1
produce put 4, size: 1
produce put 5, size: 2
produce done
consume(a) processed 2
consume(b) processed 3
consume(a) processed 4
consume(a) queue is shut down, stopping
consume(b) processed 5
consume(b) queue is shut down, stopping
results: [[0, 2, 4], [1, 3, 5]]
took 1.50s
```

## Explanation

- **Backpressure**: the queue has `maxsize=2`, and the producer has no delay of its own. Its `put()` waits whenever the queue is full, so the size never goes above 2, and items 4 and 5 are only added after the consumers take 0–3.
- **Work distribution**: two consumers take items as they become free, so each processes every other item, and 6 items × 0.5s finish in 1.5s.
- **`sentinel`**: the old way to stop consumers. The producer puts one special value (`None`) per consumer, so it has to know how many consumers there are, and the value can't be a real item.
- **`shutdown`** (3.13+): `queue.shutdown()` forbids further `put()`. Consumers still get the remaining items, and once the queue is empty, `get()` raises `QueueShutDown`. `shutdown(immediate=True)` would drop the remaining items as well.
