#!/usr/bin/env python3

import enum


@enum.unique
class Styles(str, enum.Enum):
    RESET = "\033[0m"

    BOLD = "\033[1m"
    SHADOW = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    # BLINK = "\033[6m"
    SELECTED = "\033[7m"
    TRANSPARENT = "\033[8m"
    STRIKETHROUGH = "\033[9m"


@enum.unique
class Foreground(str, enum.Enum):
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BLACK2 = "\033[90m"
    RED2 = "\033[91m"
    GREEN2 = "\033[92m"
    YELLOW2 = "\033[93m"
    BLUE2 = "\033[94m"
    MAGENTA2 = "\033[95m"
    CYAN2 = "\033[96m"
    WHITE2 = "\033[97m"


@enum.unique
class Background(str, enum.Enum):
    BLACK = "\033[40m"
    RED = "\033[41m"
    GREEN = "\033[42m"
    YELLOW = "\033[43m"
    BLUE = "\033[44m"
    MAGENTA = "\033[45m"
    CYAN = "\033[46m"
    WHITE = "\033[47m"

    BLACK2 = "\033[100m"
    RED2 = "\033[101m"
    GREEN2 = "\033[102m"
    YELLOW2 = "\033[103m"
    BLUE2 = "\033[104m"
    MAGENTA2 = "\033[105m"
    CYAN2 = "\033[106m"
    WHITE2 = "\033[107m"


def print_format_table():
    """
    prints table of formatted text format options
    """
    for style in range(8):
        for fg in range(30,38):
            s1 = ""
            for bg in range(40,48):
                format = ";".join([str(style), str(fg), str(bg)])
                s1 += "\x1b[%sm %s \x1b[0m" % (format, format)
            print(s1)
        print("\n")

# print_format_table()

for style in Styles:
    print(style.value + "Hello, World!" + Styles.RESET)

for style in Foreground:
    print(style.value + "Hello, World!" + Styles.RESET)

for style in Background:
    print(style.value + "Hello, World!" + Styles.RESET)
