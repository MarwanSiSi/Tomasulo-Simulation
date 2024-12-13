from collections import deque

from src.enums import Opcode, StationState

from .CDB import CDB
from .Instruction import Instruction
from .MemoryManager import MemoryManager
from .RegisterFile import RegisterFile
from .Station.Station import AddStation, LoadStation, MulStation, Station, StoreStation
from .Station.StationEntry import StationEntry


class Simulator:
    def __init__(self) -> None:
        self.pc: int = -1
        self.cycle: int = -1
        self.program: list[Instruction] = []
        self.memory_manager: MemoryManager = MemoryManager(self)
        self.register_file: RegisterFile = RegisterFile(self)
        self.reservation_stations: list[Station] = [
            AddStation(self, "AI", 4, 1, "AI"),
            AddStation(self, "AF", 4, 1, "AF"),
            MulStation(self, "M", 4, 1, "MF"),
            LoadStation(self, "L", 4, 1, "L"),
            StoreStation(self, "S", 4, 1, "S"),
        ]
        self.cdb = CDB()
        self.instruction_queue: deque[Instruction] = deque()

    def __str__(self) -> str:
        return f"PC: {self.pc}, Cycle: {self.cycle}"

    def __repr__(self) -> str:
        return str(self)

    def load_program(self, file_path: str) -> None:
        self.program = Instruction.parse_instructions_file(file_path)

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
        self.read_all()

    def instruction_to_station_entry(
        self,
        instruction: Instruction,
    ) -> StationEntry:
        station = StationEntry()
        station.op = instruction.opcode

        # Handle the source register (vj, qj)

        if instruction.opcode in {
            Opcode.ADD_D,
            Opcode.SUB_D,
            Opcode.MUL_D,
            Opcode.DIV_D,
            Opcode.ADD_S,
            Opcode.SUB_S,
            Opcode.MUL_S,
            Opcode.DIV_S,
        }:
            assert instruction.src is not None
            assert instruction.target is not None

            src = self.register_file.get_register(instruction.src)
            target = self.register_file.get_register(instruction.target)

            if isinstance(src, str):
                station.qj = src
            else:
                station.vj = src

            if isinstance(target, str):
                station.qk = target
            else:
                station.vk = target

        elif instruction.opcode in {Opcode.DADDI, Opcode.DSUBI}:
            assert instruction.src is not None
            assert instruction.immediate is not None

            src = self.register_file.get_register(instruction.src)

            if isinstance(src, str):
                station.qj = src
            else:
                station.vj = src

            station.a = instruction.immediate

        elif instruction.opcode in {
            Opcode.L_D,
            Opcode.L_S,
            Opcode.LW,
            Opcode.LD,
            Opcode.S_D,
            Opcode.S_S,
            Opcode.SW,
            Opcode.SD,
        }:
            assert instruction.target is not None

            target = self.register_file.get_register(instruction.target)

            if isinstance(target, str):
                station.qk = target
            else:
                station.vk = target

            if instruction.src is not None:
                src = self.register_file.get_register(instruction.src)

                if isinstance(src, str):
                    station.qj = src
                else:
                    station.vj = src
            else:
                assert instruction.immediate is not None
                station.a = instruction.immediate

        # Mark the reservation station as busy
        station.busy = True

        return station

    def issue(self) -> None:
        if len(self.instruction_queue) == 0:
            return

        instruction = self.instruction_queue[0]

        if instruction.opcode in {Opcode.BEQ, Opcode.BNE}:
            assert instruction.src is not None
            assert instruction.target is not None
            assert instruction.immediate is not None

            src = self.register_file.get_register(instruction.src)
            target = self.register_file.get_register(instruction.target)

            if isinstance(src, str):
                tag, value, _ = self.cdb.read()
                if tag == src:
                    src = value

            if isinstance(target, str):
                tag, value, _ = self.cdb.read()
                if tag == target:
                    target = value

            if isinstance(src, str) or isinstance(target, str):
                return

            if instruction.opcode == Opcode.BEQ:
                if src == target:
                    self.pc = instruction.immediate
                    self.instruction_queue.clear()

            elif instruction.opcode == Opcode.BNE:
                if src != target:
                    self.pc = instruction.immediate
                    self.instruction_queue.clear()

            return

        station_entry = self.instruction_to_station_entry(instruction)

        if station_entry.op in {Opcode.DADDI, Opcode.DSUBI}:
            result = self.reservation_stations[0].assign_entry(
                station_entry, self.cycle
            )
            if result is not None:
                assert instruction.dest is not None
                self.register_file.update_register(instruction.dest, result)

        elif station_entry.op in {
            Opcode.ADD_D,
            Opcode.ADD_S,
            Opcode.SUB_D,
            Opcode.SUB_S,
        }:
            result = self.reservation_stations[1].assign_entry(
                station_entry, self.cycle
            )
            if result is not None:
                assert instruction.dest is not None
                self.register_file.update_register(instruction.dest, result)

        elif station_entry.op in {
            Opcode.MUL_D,
            Opcode.MUL_S,
            Opcode.DIV_D,
            Opcode.DIV_S,
        }:
            result = self.reservation_stations[2].assign_entry(
                station_entry, self.cycle
            )
            if result is not None:
                assert instruction.dest is not None
                self.register_file.update_register(instruction.dest, result)

        elif station_entry.op in {Opcode.LW, Opcode.LD, Opcode.L_S, Opcode.L_D}:
            result = self.reservation_stations[3].assign_entry(
                station_entry, self.cycle
            )
            if result is not None:
                assert instruction.target is not None
                self.register_file.update_register(instruction.target, result)

        elif station_entry.op in {Opcode.SW, Opcode.SD, Opcode.S_S, Opcode.S_D}:
            result = self.reservation_stations[4].assign_entry(
                station_entry, self.cycle
            )
        else:
            raise ValueError(f"Unhandled opcode: {station_entry.op}")

        if result is not None:
            self.instruction_queue.popleft()

    def write_back(self) -> None:
        finished: list[StationEntry] = []

        for station in self.reservation_stations[:-1]:
            for entry in station.entries:
                if entry.busy and entry.state == StationState.WRITING:
                    finished.append(entry)

        finished.sort(key=lambda x: x.start_cycle)

        if len(finished) == 0:
            return

        self.cdb.write(finished[0].tag, finished[0].result)
        finished[0].busy = False
        finished[0].state = StationState.READY

    def read_all(self):
        for register in self.register_file.registers.values():
            if register.Q is not None:
                tag, value, _ = self.cdb.read()
                if tag == register.Q:
                    register.Q = None
                    register.value = value

        for staion in self.reservation_stations:
            for entry in staion.entries:
                if entry.qj is not None:
                    tag, value, _ = self.cdb.read()
                    if tag == entry.qj:
                        entry.qj = None
                        entry.vj = value

                if entry.qk is not None:
                    tag, value, _ = self.cdb.read()
                    if tag == entry.qk:
                        entry.qk = None
                        entry.vk = value
