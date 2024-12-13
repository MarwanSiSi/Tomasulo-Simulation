from collections import deque

from .Station.StationEntry import StationEntry
from src.enums import StationState

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
        self.program: list[Instruction] = []
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
        self.pc += 1

        if self.pc < len(self.program):
            self.instruction_queue.append(self.program[self.pc])

        self.issue()

        self.cdb.set_invalid()
        self.memory_manager.update()
        self.register_file.update()

        for station in self.reservation_stations:
            station.update(self.cycle)

        self.write_back()

    def issue(self) -> None:
        if len(self.instruction_queue) == 0:
            return

        instruction = self.instruction_queue[0]
        raise NotImplementedError

    def write_back(self) -> None:
        finished: list[StationEntry] = []

        for station in self.reservation_stations[:-1]:
            for entry in station.entries:
                if entry.busy and entry.state == StationState.WRITING:
                    finished.append(entry)

        finished.sort(key=lambda x: x.start_cycle)

        self.cdb.write(finished[0].tag, finished[0].result)
        finished[0].busy = False
        finished[0].state = StationState.READY
