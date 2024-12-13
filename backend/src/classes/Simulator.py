from collections import deque

from backend.src.enums.Opcode import Opcode

from .CDB import CDB
from .Instruction import Instruction
from .MemoryManager import MemoryManager
from .RegisterFile import RegisterFile
from .Station.Station import Station, AddStation, MulStation, LoadStation, StoreStation


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
        self.reservation_stations.append(AddStation("Add/Sub Int Station", 1, 1, "AI"))
        self.reservation_stations.append(AddStation("Add/Sub Float Station", 1, 1, "AF"))
        self.reservation_stations.append(MulStation("Mul/Div Float Station", 1, 1, "M"))
        self.reservation_stations.append(LoadStation("Load Station", 1, 1, "L"))
        self.reservation_stations.append(StoreStation("Store Station", 1, 1, "S"))
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

        instruction = self.instruction_queue[0]

        if instruction.opcode in {Opcode.DADDI,Opcode.DSUBI}:
            result = self.reservation_stations[0].assign_entry(instruction, self.cycle)
        elif instruction.opcode in {Opcode.ADD_D, Opcode.ADD_S, Opcode.SUB_D, Opcode.SUB_S}:
            result = self.reservation_stations[1].assign_entry(instruction, self.cycle)
        elif instruction.opcode in {Opcode.MUL_D, Opcode.MUL_S, Opcode.DIV_D, Opcode.DIV_S}:
            result = self.reservation_stations[2].assign_entry(instruction, self.cycle)
        elif instruction.opcode in {Opcode.LW, Opcode.LD, Opcode.L_S, Opcode.L_D}:
            result = self.reservation_stations[3].assign_entry(instruction, self.cycle)
        elif instruction.opcode in {Opcode.SW, Opcode.SD, Opcode.S_S, Opcode.S_D}:
            result = self.reservation_stations[4].assign_entry(instruction, self.cycle)

        if result:
            self.instruction_queue.popleft()
        raise NotImplementedError
