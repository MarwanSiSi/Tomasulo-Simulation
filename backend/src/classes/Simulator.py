from collections import deque

from .CDB import CDB
from .Instruction import Instruction
from .MemoryManager import MemoryManager
from .RegisterFile import RegisterFile


class Simulator:
    def __init__(self) -> None:
        self.pc: int = 0
        self.cycle: int = 0
        self.program: str = ""
        self.memory_manager: MemoryManager = MemoryManager()
        self.register_file: RegisterFile = RegisterFile()
        self.reservation_stations: list = []
        self.cdb = CDB.get_instance()
        self.instruction_queue: deque[Instruction] = deque()

    def update(self) -> None:
        self.cycle += 1
        self.cdb.set_invalid()
        self.memory_manager.update()
        self.register_file.update()

    def issue(self) -> None:
        if len(self.instruction_queue) == 0:
            return

        instruction = self.instruction_queue.popleft()
        raise NotImplementedError
