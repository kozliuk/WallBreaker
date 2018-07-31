import time
import asyncio
from multiprocessing import Process
from threading import Thread

from wallbreaker import WallBreaker


async def input_consumer(_wb):
    while True:
        item = await _wb.input_get()
        print(">>", item)


async def output_producer(_wb):
    while True:
        _wb.output_put({"message": "input from process"})
        await asyncio.sleep(1)


def process(_wb):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([input_consumer(_wb), output_producer(_wb)]))


def input_producer(_wb):
    while True:
        _wb.input_put({"message": "input from main"})
        time.sleep(1)


def output_consumer(_wb):
    while True:
        item = _wb.output_get()
        print("<<", item)


def main():
    wb = WallBreaker()
    Process(target=process, args=(wb,)).start()
    Thread(target=input_producer, args=(wb, )).start()
    Thread(target=output_consumer, args=(wb, )).start()


if __name__ == '__main__':
    main()
