from abc import ABC, abstractmethod

from src.utils import execute_station_entry

from ..CDB import CDB
from .StationEntry import StationEntry


class Station(ABC):
    def __init__(self, name: str, size: int, latency: int, prefex: str):
        self.name = name
        self.size = size  # Number of slots in the station
        self.latency = latency
        self.entries: list[StationEntry] = [
            StationEntry(f"{prefex}{i + 1}", 0) for i in range(size)
        ]
        self.cdb = CDB.get_instance()

    def __str__(self):
        return f"{self.name} (Size: {self.size})"

    def __repr__(self):
        return f"{self.name} (Size: {self.size})"

    @abstractmethod
    def update(self, time: int):
        """Updates the station logic, including checking readiness and executing entries."""
        pass

    def assign_entry(self, entry: StationEntry) -> bool:
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
            print(f"{self.name}: Assigned entry {entry}")
            return True

        print(f"{self.name}: No available slots to assign entry {entry}.")
        return False

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
        tag, value, valid = self.cdb.read()

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

            if entry.cycles_remaining > 0:  # Decrement cycles
                entry.cycles_remaining -= 1
                print(
                    f"{self.name}: ADD/SUB in progress at slot {index}, "
                    f"cycles remaining = {entry.cycles_remaining}."
                )
            else:  # Execute if all cycles are completed
                try:
                    result = execute_station_entry(entry)
                    print(
                        f"{self.name}: Executed ADD/SUB at slot {index}, result = {result}."
                    )
                    self.complete_entry(index)
                except Exception as e:
                    print(f"{self.name}: Error at slot {index}: {e}")


class MulStation(Station):
    """Handles multiplication and division operations."""

    def update(self, time: int):
        """Simulates the execution of multiplication and division instructions over user-defined cycles."""
        tag, value, valid = self.cdb.read()

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

            if entry.cycles_remaining > 0:  # Decrement cycles
                entry.cycles_remaining -= 1
                print(
                    f"{self.name}: MUL/DIV in progress at slot {index}, "
                    f"cycles remaining = {entry.cycles_remaining}."
                )
            else:  # Execute if all cycles are completed
                try:
                    result = execute_station_entry(entry)
                    print(
                        f"{self.name}: Executed MUL/DIV at slot {index}, result = {result}."
                    )
                    self.complete_entry(index)
                except ZeroDivisionError as e:
                    print(f"{self.name}: Division by zero at slot {index}: {e}")
                except Exception as e:
                    print(f"{self.name}: Error at slot {index}: {e}")


class LoadStation(Station):
    """Handles load operations."""

    def update(self, time: int):
        """Simulates the execution of load instructions over user-defined cycles."""
        tag, value, valid = self.cdb.read()

        for index, entry in enumerate(self.entries):
            if not entry.busy:
                continue

            if entry.qj is not None:
                if not valid:
                    continue

                if entry.qj == tag:
                    entry.vj = value
                    entry.qj = None

                continue

            if entry.cycles_remaining > 0:  # Decrement cycles
                entry.cycles_remaining -= 1
                print(
                    f"{self.name}: LOAD in progress at slot {index}, "
                    f"cycles remaining = {entry.cycles_remaining}."
                )
            else:  # Execute if all cycles are completed
                try:
                    result = entry.a
                    print(
                        f"{self.name}: Executed LOAD at slot {index}, value = {result}."
                    )
                    self.complete_entry(index)
                except Exception as e:
                    print(f"{self.name}: Error at slot {index}: {e}")


class StoreStation(Station):
    """Handles store operations."""

    def update(self, time: int):
        """Simulates the execution of store instructions over user-defined cycles."""
        tag, value, valid = self.cdb.read()

        for index, entry in enumerate(self.entries):
            if not entry.busy:
                continue

            if entry.qj is None:
                if not valid:
                    continue

                if entry.qj == tag:
                    entry.vj = value
                    entry.qj = None

                continue

            if entry.cycles_remaining > 0:  # Decrement cycles
                entry.cycles_remaining -= 1
                print(
                    f"{self.name}: STORE in progress at slot {index}, "
                    f"cycles remaining = {entry.cycles_remaining}."
                )
            else:  # Execute if all cycles are completed
                try:
                    # Perform store operation; for now, we assume it succeeds
                    print(
                        f"{self.name}: Executed STORE at slot {index}, value = {entry.a}."
                    )
                    self.complete_entry(index)
                except Exception as e:
                    print(f"{self.name}: Error at slot {index}: {e}")
