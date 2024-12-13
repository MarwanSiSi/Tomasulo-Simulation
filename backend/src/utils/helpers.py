from src.enums import Opcode
from src.classes.StationEntry import StationEntry


def execute_station_entry(entry: StationEntry) -> int | float:
    """
    Executes the operation in a station entry.
    Returns the result of the operation or None if execution cannot proceed.
    """
    if not entry.busy or not entry.op:
        raise ValueError(f"StationEntry {entry} is idle or missing an operation.")

    if entry.qj is not None or entry.qk is not None:  # Both sources are ready
        raise ValueError(f"StationEntry {entry} is not ready to execute.")

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
        immediate = entry.a

        if entry.op == Opcode.DADDI:
            return entry.vj + immediate
        else:
            return entry.vj - immediate
    else:
        raise ValueError(f"Invalid opcode {entry.op}")
