import asyncio
from multiprocessing import Queue


class WallBreaker:

    def __init__(self):
        self.input = Queue()
        self.output = Queue()
        self.async_input = None
        self.loop = None

    async def get_async_input_queue(self):
        return self.async_input

    def input_put(self, item):
        self.input.put(item)

    async def input_get(self):
        if self.loop is None:
            self.loop = asyncio.get_event_loop()

        if self.async_input is None:
            self.async_input = asyncio.Queue()

            def _loop():
                while True:
                    item = self.input.get()
                    f = asyncio.run_coroutine_threadsafe(self.async_input.put(item), self.loop)
                    f.result()

            self.loop.run_in_executor(None, _loop)

        return await self.async_input.get()

    def output_get(self):
        return self.output.get()

    def output_put(self, item):
        self.output.put(item)
