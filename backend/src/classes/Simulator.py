from collections import deque

from .CDB import CDB
from .Instruction import Instruction
from .MemoryManager import MemoryManager
from .RegisterFile import RegisterFile
from .Station.Station import Station


class Simulator:
    __loaded = False
    __instance = None

    def __init__(self) -> None:
        if self.__instance is not None and not self.__loaded:
            raise Exception("This class is a singleton!")

        self.__instance = self
        self.pc: int = 0
        self.cycle: int = 0
        self.program: str = ""
        self.memory_manager: MemoryManager = MemoryManager()
        self.register_file: RegisterFile = RegisterFile()
        self.reservation_stations: list[Station] = []
        self.cdb = CDB()
        self.instruction_queue: deque[Instruction] = deque()

    @staticmethod
    def get_instance() -> "Simulator":
        if Simulator.__instance is None:
            Simulator.__loaded = True
            Simulator.__instance = Simulator()

        return Simulator.__instance

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
