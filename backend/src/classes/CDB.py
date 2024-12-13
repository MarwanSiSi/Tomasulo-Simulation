from src.exceptions import CDBException


class CDB:
    __instance = None

    def __init__(self) -> None:
        if CDB.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CDB.__instance = self
            self.__tag: str = ""
            self.__data: int | float = 0
            self.__valid: bool = False

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

    @staticmethod
    def get_instance() -> "CDB":
        if CDB.__instance is None:
            CDB.__instance = CDB()
        return CDB.__instance
