from src.exceptions import MemoryAccessException


class Cache:
    def __init__(self):
        self.__cache: dict[int, int | float] = {}

    def contains(self, address: int) -> bool:
        return address in self.__cache

    def read(self, address: int) -> int | float:
        try:
            return self.__cache[address]
        except KeyError as e:
            raise MemoryAccessException(address) from e

    def write(self, address: int, value: int | float):
        self.__cache[address] = value
