from src.enums import Opcode, StationState


class StationEntry:
    def __init__(self, tag: str = "", cycles_required: int = 0) -> None:
        self.tag: str = tag
        self.state: StationState = StationState.READY
        self.busy = False
        self.op: Opcode | None = None
        self.vj: int | float = 0
        self.vk: int | float = 0
        self.qj: str | None = None
        self.qk: str | None = None
        self.a: int = 0
        self.result: int | float = 0
        self.start_cycle: int = 0
        self.cycles_remaining: int = cycles_required

    def __str__(self) -> str:
        return f"{self.tag}: {self.state} {self.op} {self.vj} {self.vk} {self.qj} {self.qk} {self.a} {self.result} {self.start_cycle} {self.cycles_remaining}"

    def __repr__(self) -> str:
        return self.__str__()

    def reset(self) -> None:
        self.busy = False
        self.state = StationState.READY
        self.op = None
        self.vj = 0
        self.vk = 0
        self.qj = None
        self.qk = None
        self.a = 0
        self.result = 0
        self.start_cycle = 0
        self.cycles_remaining = 0
        self.start_cycle = 0
        self.result = 0
