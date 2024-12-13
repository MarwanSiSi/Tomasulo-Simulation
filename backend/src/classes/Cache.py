from collections import OrderedDict

from src.exceptions import MemoryAccessException


class Cache:
    def __init__(self):
        self.cache = OrderedDict()

    def __str__(self) -> str:
        return "\n".join(
            [f"{address}: {value}" for address, value in self.cache.items()]
        )

    def __repr__(self) -> str:
        return self.__str__()

    def contains(self, address: int) -> bool:
        return address in self.cache

    def read(self, address: int) -> int | float:
        try:
            return self.cache[address]
        except KeyError as e:
            raise MemoryAccessException(address) from e

    def write(self, address: int, value: int | float):
        self.cache[address] = value
