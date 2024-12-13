from typing import Protocol
from src.exceptions import CDBException


class CDB:
    class CDBProtocol(Protocol):
        tag: str
        start_cycle: int
        result: int | float

    def __init__(self) -> None:
        self.__tag: str = ""
        self.__data: int | float = 0
        self.__valid: bool = False

    def reset(self) -> None:
        self.__tag = ""
        self.__data = 0
        self.__valid = False

    def set_invalid(self) -> None:
        self.__valid = False

    def write(self, tag: str, data: int | float) -> None:
        if self.__valid:
            raise CDBException("CDB is busy!")

        self.__tag = tag
        self.__data = data
        self.__valid = True

    def read(self) -> tuple[str, int | float, bool]:
        return self.__tag, self.__data, self.__valid
