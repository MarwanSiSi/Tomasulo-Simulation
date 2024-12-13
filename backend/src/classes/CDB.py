class CDB:
    __instance = None

    def __init__(self) -> None:
        self.tag: str = ""
        self.data: int | float = 0
        self.valid: bool = False

    def write(self, tag: str, data: int | float) -> None:
        self.tag = tag
        self.data = data
        self.valid = True

    def read(self) -> tuple[str, int | float, bool]:
        return self.tag, self.data, self.valid

    @staticmethod
    def get_instance() -> "CDB":
        if CDB.__instance is None:
            CDB.__instance = CDB()
        return CDB.__instance
