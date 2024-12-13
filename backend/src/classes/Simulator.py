from .MemoryManager import MemoryManager
from .RegisterFile import RegisterFile
from .CDB import CDB


class Simulator:
    def __init__(self) -> None:
        self.pc: int = 0
        self.cycle: int = 0
        self.program: str = ""
        self.memory_manager: MemoryManager = MemoryManager()
        self.register_file: RegisterFile = RegisterFile()
        self.reservation_stations: list = []
        self.cdb = CDB.get_instance()

    def update(self) -> None:
        self.cycle += 1
        self.cdb.set_invalid()
        self.memory_manager.update()
        self.register_file.update()
