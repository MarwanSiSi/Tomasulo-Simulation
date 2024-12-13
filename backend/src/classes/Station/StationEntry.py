from src.enums import Opcode


class StationEntry:
    def __init__(self, cycles_required: int) -> None:
        self.busy = False
        self.op = None
        self.vj = None
        self.vk = None
        self.qj = None
        self.qk = None
        self.cycles_remaining = cycles_required