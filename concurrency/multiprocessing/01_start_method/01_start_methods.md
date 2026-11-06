# 01_start_methods

## Output

```
module imported in pid 66146 as __main__
main pid 66146
default start method: forkserver

--- fork ---
child: pid 66147, parent 66146, config: changed at runtime
took 0.003s

--- spawn ---
module imported in pid 66150 as __mp_main__
child: pid 66150, parent 66146, config: initial
took 0.072s

--- forkserver ---
module imported in pid 66152 as __mp_main__
child: pid 66153, parent 66152, config: initial
took 0.069s

--- forkserver ---
child: pid 66155, parent 66152, config: initial
took 0.008s
```

## Explanation

- **Default**: since 3.14 the default start method on Linux is `forkserver`; before that it was `fork`. macOS and Windows already used `spawn`. `mp.get_context(method)` gives the multiprocessing API bound to one start method without changing the global default.
- **`fork`**: the child is a copy of the parent process at the moment of `start()`. It's the fastest (3ms) and sees `config` as changed at runtime, and the module isn't imported again. It's unsafe when the parent has threads, since only the calling thread is copied, and a lock held by another thread stays locked forever in the child. That's the reason the default changed.
- **`spawn`**: starts a fresh Python interpreter that imports the main module again (as `__mp_main__`, so the `__name__ == '__main__'` block doesn't run). It's the slowest (~70ms) and sees only `config = 'initial'`. Everything the child needs must come through arguments, which are pickled.
- **`forkserver`**: on first use, a clean server process is started (pid 66152) and imports the module once. Every child is then forked from that server, not from the main process; note that `parent` is the server's pid. The first start is slow because it includes starting the server, and later ones are almost as fast as `fork` (8ms). Children are as clean as with `spawn`.

The `if __name__ == '__main__':` guard is required for `spawn` and `forkserver`. Without it, the re-imported module would start processes again.
