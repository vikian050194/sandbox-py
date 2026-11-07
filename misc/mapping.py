#!/usr/bin/env python3

from pprint import pp

class Foo():
    def __init__(self, bar):
        self.bar = bar


    def __str__(self):
        return f"Foo.bar={self.bar}"


    def __repr__(self):
        return f"Foo(bar={self.bar})"

arr = ["a", "b", "c"]

brr = list(map(Foo, arr))

pp(brr)