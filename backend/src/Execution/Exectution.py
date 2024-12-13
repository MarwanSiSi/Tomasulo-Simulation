from src.enums import Opcode
from src.classes import StationEntry


def execute_station_entry(entry: StationEntry) -> int | None:
    """
    Executes the operation in a station entry.
    Returns the result of the operation or None if execution cannot proceed.
    """
    if entry.busy and entry.op:
        if entry.qj is None and entry.qk is None:  # Both sources are ready
            if entry.op in {Opcode.ADD_D, Opcode.ADD_S}:
                return entry.vj + entry.vk
            elif entry.op in {Opcode.SUB_D, Opcode.SUB_S}:
                return entry.vj - entry.vk
            elif entry.op in {Opcode.MUL_D, Opcode.MUL_S}:
                return entry.vj * entry.vk
            elif entry.op in {Opcode.DIV_D, Opcode.DIV_S}:
                if entry.vk != 0:
                    return entry.vj / entry.vk
                else:
                    raise ZeroDivisionError(f"Division by zero for opcode {entry.op}")
            elif entry.op in {Opcode.DADDI, Opcode.DSUBI}:
                if entry.a is not None:
                    immediate = entry.a
                    if entry.op == Opcode.DADDI:
                        return entry.vj + immediate
                    elif entry.op == Opcode.DSUBI:
                        return entry.vj - immediate
        else:
            print(f"StationEntry {entry} is not ready. Waiting for operands.")
            return None
    else:
        print(f"StationEntry {entry} is idle or missing an operation.")
        return None

