from src.enums import Opcode
from src.classes.StationEntry import StationEntry
from src.utils.helpers import execute_station_entry


if __name__ == "__main__":
    entry = StationEntry()
    entry.busy = True
    entry.op = Opcode.ADD_D
    entry.vj = 5
    entry.vk = 3
    result = execute_station_entry(entry)
    if result is not None:
        print(f"Execution result: {result}")
