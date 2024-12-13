from src.enums import Opcode


class StationEntry:
    def __init__(self) -> None:
        self.busy: bool = False
        self.op: Opcode
        self.vj: int = 0
        self.vk: int = 0
        self.qj: str | None = None
        self.qk: str | None = None
        self.a: int = 0
