#!/usr/bin/env python3

import sys
import signal
import asyncio

KEYBOARD_INTERRUPT = False
INTERRUPT_SAFE = False
WS_CLIENT = None

def sigint_handler(signal, frame):
    global KEYBOARD_INTERRUPT, INTERRUPT_SAFE
    print(f'handle interrupt sig {signal} {INTERRUPT_SAFE}')
    if INTERRUPT_SAFE:
        KEYBOARD_INTERRUPT = True
    else:
        if WS_CLIENT:
            WS_CLIENT.exit()
        sys.exit(0)


async def testFunction():
    global KEYBOARD_INTERRUPT

    while not KEYBOARD_INTERRUPT:
        print("before")
        await asyncio.sleep(5)
        print("after")


def main():
    global INTERRUPT_SAFE, WS_CLIENT

    # WS_CLIENT = connect()

    signal.signal(signal.SIGINT, sigint_handler)

    INTERRUPT_SAFE=True
    asyncio.run(testFunction())
    INTERRUPT_SAFE=False

if __name__ == '__main__':
    main()
