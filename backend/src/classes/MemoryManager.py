from dataclasses import dataclass

from .Cache import Cache
from .CDB import CDB
from src.exceptions import MemoryAccessException, CDBException


class MemoryManager:
    @dataclass
    class Request:
        tag: str
        stime: int
        ctime: int
        etime: int
        address: int
        value: int | float

    def __init__(self, latency: int = 1, penalty: int = 5, block_size: int = 1024):
        self.latency = latency
        self.penalty = penalty
        self.block_size = block_size
        self.cache = Cache()
        self.data_memory: dict[int, int | float] = {}
        self.instruction_memory: dict[int, int | float] = {}
        self.requests: list[MemoryManager.Request] = []
        self.cdb = CDB.get_instance()

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
                value = 0
                try:
                    value = self.cache.read(address)
                except MemoryAccessException:
                    request.etime += self.penalty
                    continue

                try:
                    self.cdb.write(tag, value)
                    self.requests.remove(request)
                except CDBException:
                    pass
            elif tag.upper().startswith("S"):
                try:
                    self.cache.write(address, value)
                    self.requests.remove(request)
                except MemoryAccessException:
                    request.etime += self.penalty
                    continue

    def request_write(self, tag: str, address: int, value: int | float, ctime: int):
        stime = ctime
        etime = self.latency

        self.requests.append(
            MemoryManager.Request(tag, stime, ctime, etime, address, value)
        )

    def request_read(self, tag: str, address: int, ctime: int):
        stime = ctime
        etime = self.latency

        self.requests.append(
            MemoryManager.Request(tag, stime, ctime, etime, address, 0)
        )

    def transfer_to_cache(self, address: int):
        if self.cache.contains(address):
            return

        start = address - address % self.block_size
        end = start + self.block_size

        for i in range(start, end):
            self.cache.write(i, self.data_memory.get(i, 0))
