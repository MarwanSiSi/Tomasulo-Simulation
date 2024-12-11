from enum import Enum


class StationState(Enum):
    READY = "ready"
    ISSUED = "issued"
    WAITING = "waiting"
    EXECUTING = "executing"
    WRITING = "writing"
