from src.exceptions import MemoryAccessException


class Cache:
    def __init__(self):
        self.cache: dict[int, int | float] = {}

    def read(self, address: int) -> int | float:
        try:
            return self.cache[address]
        except KeyError as e:
            raise MemoryAccessException(address) from e

    def write(self, address: int, value: int | float):
        self.cache[address] = value
