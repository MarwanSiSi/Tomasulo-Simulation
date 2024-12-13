from dataclasses import dataclass

from src.exceptions import MemoryAccessException

from .Cache import Cache


class MemoryManager:
    @dataclass
    class Request:
        tag: str
        start_cycle: int
        current_cycle: int
        end_cycle: int
        address: int
        value: int | float | None = None
        result: int | float | None = None
        done: bool = False

    def __init__(
        self, simulator, latency: int = 1, penalty: int = 5, block_size: int = 1024
    ):
        self.latency = latency
        self.penalty = penalty
        self.block_size = block_size
        self.cache = Cache()
        self.data_memory: dict[int, int | float] = {}
        self.requests: dict[str, MemoryManager.Request] = {}
        self.simulator = simulator

    def update(self):
        for tag, request in self.requests.copy().items():
            stime = request.start_cycle
            ctime = request.current_cycle
            etime = request.end_cycle
            address = request.address
            value = request.value
            request.current_cycle += 1

            if (ctime - stime) != etime:
                continue

            if etime == self.latency + self.penalty:
                self.transfer_to_cache(address)

            if tag.upper().startswith("L"):
                try:
                    request.result = self.cache.read(address)
                    request.done = True
                except MemoryAccessException:
                    request.end_cycle += self.penalty
            elif tag.upper().startswith("S"):
                try:
                    self.cache.write(address, value or 0)
                    request.done = True
                except MemoryAccessException:
                    request.end_cycle += self.penalty
            else:
                raise ValueError(f"Invalid tag: {tag}")

    def request_store(self, tag: str, address: int, value: int | float, ctime: int):
        stime = ctime
        etime = self.latency

        self.requests[tag] = MemoryManager.Request(
            tag, stime, ctime, etime, address, value
        )

    def request_load(self, tag: str, address: int, ctime: int):
        stime = ctime
        etime = self.latency

        self.requests[tag] = MemoryManager.Request(
            tag,
            stime,
            ctime,
            etime,
            address,
        )

    def transfer_to_cache(self, address: int):
        if self.cache.contains(address):
            return

        start = address - address % self.block_size
        end = start + self.block_size

        for i in range(start, end):
            self.cache.write(i, self.data_memory.get(i, 0))
