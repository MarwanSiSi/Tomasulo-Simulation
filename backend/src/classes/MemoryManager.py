from dataclasses import dataclass

from src.exceptions import MemoryAccessException

from .Cache import Cache
from .Simulator import Simulator


class MemoryManager:
    @dataclass
    class Request:
        tag: str
        stime: int
        ctime: int
        etime: int
        address: int
        value: int | float | None

    def __init__(self, latency: int = 1, penalty: int = 5, block_size: int = 1024):
        self.latency = latency
        self.penalty = penalty
        self.block_size = block_size
        self.cache = Cache()
        self.data_memory: dict[int, int | float] = {}
        self.instruction_memory: dict[int, int | float] = {}
        self.requests: list[MemoryManager.Request] = []
        self.simulatior = Simulator.get_instance()

    def update(self):
        for request in self.requests[:]:
            tag = request.tag
            stime = request.stime
            ctime = request.ctime
            etime = request.etime
            address = request.address
            value = request.value
            request.ctime += 1

            if (ctime - stime) != etime:
                continue

            if etime == self.latency + self.penalty:
                self.transfer_to_cache(address)

            if tag.upper().startswith("L"):
                try:
                    request.value = self.cache.read(address)
                except MemoryAccessException:
                    request.etime += self.penalty
            elif tag.upper().startswith("S"):
                try:
                    self.cache.write(address, value or 0)
                    self.requests.remove(request)
                except MemoryAccessException:
                    request.etime += self.penalty
            else:
                raise ValueError(f"Invalid tag: {tag}")

    def request_store(self, tag: str, address: int, value: int | float, ctime: int):
        stime = ctime
        etime = self.latency

        self.requests.append(
            MemoryManager.Request(tag, stime, ctime, etime, address, value)
        )

    def request_load(self, tag: str, address: int, ctime: int):
        stime = ctime
        etime = self.latency

        self.requests.append(
            MemoryManager.Request(tag, stime, ctime, etime, address, None)
        )

    def transfer_to_cache(self, address: int):
        if self.cache.contains(address):
            return

        start = address - address % self.block_size
        end = start + self.block_size

        for i in range(start, end):
            self.cache.write(i, self.data_memory.get(i, 0))
