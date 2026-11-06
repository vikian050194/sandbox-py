# 04_exception_group

## Output

```
--- one_type ---
fetch(a) started
fetch(b) started
fetch(c) started
fetch(b) failed after 1s with ValueError
fetch(c) cancelled
fetch(a) cancelled
handled ValueError: (ValueError('b failed'),)
took 1.03s

--- two_types ---
fetch(a) started
fetch(b) started
fetch(c) started
fetch(b) failed after 1s with ValueError
fetch(c) failed after 1s with TypeError
fetch(a) cancelled
handled ValueError: (ValueError('b failed'),)
handled TypeError: (TypeError('c failed'),)
took 1.00s

--- unexpected_type ---
fetch(a) started
fetch(b) started
fetch(c) started
fetch(b) failed after 1s with KeyError
fetch(c) cancelled
fetch(a) cancelled
handled other: (KeyError('b failed'),)
took 1.00s
```

## Explanation

- **`one_type`**: a single `ValueError` arrives inside an `ExceptionGroup`. `except* ValueError` matches the error inside the group, not the group itself, so it handles it the way `except ValueError` would handle a plain error.
- **`two_types`**: `b` and `c` fail at the same moment, so both errors make it into the group before the TaskGroup starts cancelling (only `a` gets cancelled). Both `except* ValueError` and `except* TypeError` run. With a plain `except`, only the first matching clause would run.
- **What each clause receives**: `eg` in every clause is a new `ExceptionGroup` containing only the errors of that type. `eg.exceptions` is the tuple of those errors.
- **`unexpected_type`**: a `KeyError` matches neither specific clause and ends up in `except* Exception`, which works as a catch-all for whatever is left. Without that clause, the unmatched part would be re-raised as an `ExceptionGroup` after the other clauses run.

`except` and `except*` can't be mixed in the same `try` statement.
