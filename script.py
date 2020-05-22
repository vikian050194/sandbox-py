#!/usr/bin/env python3

"""Module docstring"""

def generate_file(min = 0, max = 10):
    output = "output.txt"

    lines = []

    for x in range(min, max + 1):
        lines.append(f"{x}\n")

    with open(output, 'w') as out_file:
        out_file.writelines(lines)

if __name__ == "__main__":
    generate_file()
