from typing import Sequence


def starts_with_frog(seq: Sequence[str]) -> bool:
    match seq:
        case ["🐸", *_]: return True
        case _: return False

print(starts_with_frog(["🐸", "🐛", "🦋", "🪲"]))  # True
print(starts_with_frog(["🐛", "🦋", "🪲"])) # False

print(starts_with_frog(("🐸", "🐛", "🦋", "🪲")))  # True

print(starts_with_frog(None)) # False
print(starts_with_frog("ribbit")) # False
print(starts_with_frog("🐸")) # False