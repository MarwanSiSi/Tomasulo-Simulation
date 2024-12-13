from abc import ABC, abstractmethod

from src.utils import execute_station_entry

from .StationEntry import StationEntry
from src.enums.StationState import StationState


class Station(ABC):
    def __init__(self, simulator, name: str, size: int, latency: int, prefex: str):
        self.name = name
        self.size = size  # Number of slots in the station
        self.latency = latency
        self.entries: list[StationEntry] = [
            StationEntry(f"{prefex}{i + 1}", latency) for i in range(size)
        ]
        self.simulator = simulator

    def set_size(self, size: int):
        self.size = size
        self.entries = [
            StationEntry(f"{self.name}{i + 1}", self.latency) for i in range(size)
        ]

    def __str__(self):
        return f"{self.name}: {self.entries}"

    def __repr__(self):
        return str(self)

    @abstractmethod
    def update(self, time: int):
        """Updates the station logic, including checking readiness and executing entries."""
        pass

    def assign_entry(self, entry: StationEntry, time: int) -> str | None:
        """
        Assigns a new entry to the station if a slot is available.
        Returns True if the entry is successfully assigned; False otherwise.
        """
        for station_entry in self.entries:
            if station_entry.busy:
                continue

            station_entry.busy = True
            station_entry.op = entry.op
            station_entry.vj = entry.vj
            station_entry.vk = entry.vk
            station_entry.qj = entry.qj
            station_entry.qk = entry.qk
            station_entry.a = entry.a
            station_entry.cycles_remaining = self.latency
            station_entry.state = StationState.ISSUED
            station_entry.start_cycle = time

            return station_entry.tag

        return None

    def complete_entry(self, index: int):
        """Marks the entry at the given index as completed."""
        if 0 <= index < self.size and self.entries[index].busy:
            self.entries[index].reset()
        else:
            raise ValueError(f"Invalid slot index {index} or slot is not busy.")


class AddStation(Station):
    """Handles addition and subtraction operations."""

    def update(self, time: int):
        """Simulates the execution of addition and subtraction instructions over user-defined cycles."""
        tag, value, valid = self.simulator.cdb.read()

        for index, entry in enumerate(self.entries):
            if not entry.busy:
                continue

            if entry.qj is not None or entry.qk is not None:  # Check readiness
                if not valid:
                    continue

                if entry.qj == tag:
                    entry.vj = value
                    entry.qj = None
                if entry.qk == tag:
                    entry.vk = value
                    entry.qk = None

                continue

            if entry.state == StationState.ISSUED:
                entry.state = StationState.WAITING
                return

            if entry.cycles_remaining > 0:  # Decrement cycles
                entry.cycles_remaining -= 1
                entry.state = StationState.EXECUTING
            else:  # Execute if all cycles are completed
                try:
                    result = execute_station_entry(entry)
                    entry.result = result
                    entry.state = StationState.WRITING
                except Exception as e:
                    print(f"{self.name}: Error at slot {index}: {e}")


class MulStation(Station):
    """Handles multiplication and division operations."""

    def update(self, time: int):
        """Simulates the execution of multiplication and division instructions over user-defined cycles."""
        tag, value, valid = self.simulator.cdb.read()

        for index, entry in enumerate(self.entries):
            if not entry.busy:
                continue

            if entry.qj is not None or entry.qk is not None:  # Check readiness
                if not valid:
                    continue

                if entry.qj == tag:
                    entry.vj = value
                    entry.qj = None
                if entry.qk == tag:
                    entry.vk = value
                    entry.qk = None

                continue

            if entry.state == StationState.ISSUED:
                entry.state = StationState.WAITING
                return

            if entry.cycles_remaining > 0:  # Decrement cycles
                entry.cycles_remaining -= 1
                entry.state = StationState.EXECUTING
            else:  # Execute if all cycles are completed
                try:
                    result = execute_station_entry(entry)
                    entry.result = result
                    entry.state = StationState.WRITING
                except ZeroDivisionError as e:
                    print(f"{self.name}: Division by zero at slot {index}: {e}")
                except Exception as e:
                    print(f"{self.name}: Error at slot {index}: {e}")


class LoadStation(Station):
    """Handles load operations."""

    def update(self, time: int):
        """Simulates the execution of load instructions over user-defined cycles."""
        tag, value, valid = self.simulator.cdb.read()

        for entry in self.entries:
            if not entry.busy:
                continue

            if entry.qj is not None:
                if not valid:
                    continue

                if entry.qj == tag:
                    entry.a = int(value)
                    entry.qj = None

                continue

            if entry.state == StationState.ISSUED:
                entry.state = StationState.WAITING
                return

            mem_request = self.simulator.memory_manager.requests.get(entry.tag, None)
            if mem_request is not None and mem_request.result is not None:
                entry.result = mem_request.result
                entry.state = StationState.WRITING
            elif mem_request is None:
                self.simulator.memory_manager.request_load(entry.tag, entry.a, time)
                entry.state = StationState.EXECUTING


class StoreStation(Station):
    """Handles store operations."""

    def update(self, time: int):
        """Simulates the execution of store instructions over user-defined cycles."""
        tag, value, valid = self.simulator.cdb.read()

        for entry in self.entries:
            if not entry.busy:
                continue

            if entry.qj is None or entry.qk is not None:
                if not valid:
                    continue

                if entry.qj == tag:
                    entry.vj = int(value)
                    entry.qj = None

                if entry.qk == tag:
                    entry.a = int(value)
                    entry.qk = None

                continue

            if entry.state == StationState.ISSUED:
                entry.state = StationState.WAITING
                return

            mem_request = self.simulator.memory_manager.requests.get(entry.tag, None)
            if mem_request is not None and mem_request.done:
                entry.state = StationState.WRITING
            elif mem_request is None:
                self.simulator.memory_manager.request_store(
                    entry.tag, entry.a, entry.vj, time
                )
                entry.state = StationState.EXECUTING
