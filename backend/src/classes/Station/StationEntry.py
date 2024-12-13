from src.enums import Opcode


class StationEntry:
    def __init__(self, tag: str, cycles_required: int) -> None:
        self.tag: str = tag
        self.busy = False
        self.op: Opcode | None = None
        self.vj: int | float = 0
        self.vk: int | float = 0
        self.qj: str | None = None
        self.qk: str | None = None
        self.a: int | float = 0
        self.cycles_remaining: int = cycles_required

    def reset(self) -> None:
        self.busy = False
        self.op = None
        self.vj = 0
        self.vk = 0
        self.qj = None
        self.qk = None
        self.a = 0
        self.cycles_remaining = 0
