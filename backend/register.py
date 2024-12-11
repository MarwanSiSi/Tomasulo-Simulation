from enum import Enum
from typing import Union


class Registers(Enum):
    R0 = "R0"
    R1 = "R1"
    R2 = "R2"
    R3 = "R3"
    R4 = "R4"
    R5 = "R5"
    R6 = "R6"
    R7 = "R7"
    R8 = "R8"
    R9 = "R9"
    R10 = "R10"
    R11 = "R11"
    R12 = "R12"
    R13 = "R13"
    R14 = "R14"
    R15 = "R15"
    R16 = "R16"
    R17 = "R17"
    R18 = "R18"
    R19 = "R19"
    R20 = "R20"
    R21 = "R21"
    R22 = "R22"
    R23 = "R23"
    R24 = "R24"
    R25 = "R25"
    R26 = "R26"
    R27 = "R27"
    R28 = "R28"
    R29 = "R29"
    R30 = "R30"
    R31 = "R31"
    F0 = "F0"
    F1 = "F1"
    F2 = "F2"
    F3 = "F3"
    F4 = "F4"
    F5 = "F5"
    F6 = "F6"
    F7 = "F7"
    F8 = "F8"
    F9 = "F9"
    F10 = "F10"
    F11 = "F11"
    F12 = "F12"
    F13 = "F13"
    F14 = "F14"
    F15 = "F15"
    F16 = "F16"
    F17 = "F17"
    F18 = "F18"
    F19 = "F19"
    F20 = "F20"
    F21 = "F21"
    F22 = "F22"
    F23 = "F23"
    F24 = "F24"
    F25 = "F25"
    F26 = "F26"
    F27 = "F27"
    F28 = "F28"
    F29 = "F29"
    F30 = "F30"
    F31 = "F31"

class Register:
    def __init__(self, name: Registers, value: float = 0.0, Q: Union[str, None] = None):
        """
        Initialize a register with a name, value, and optional reservation station tag (Q).
        :param name: The name of the register.
        :param value: The initial value of the register (default is 0.0).
        :param Q: The reservation station tag, which can be a string (default is None).
        """
        self.name = name
        self.value = value
        self.Q = Q  # The reservation station tag can be a string or None.

    def get(self):
        """Returns the value or reservation station tag (Q) of the register."""
        return self.Q if self.Q is not None else self.value

    def update(self, value_or_tag: Union[float, str]):
        """Updates the register's value or reservation station tag."""
        if isinstance(value_or_tag, (int, float)):
            self.value = value_or_tag
            self.Q = None  # Clear Q when directly updating the value
        elif isinstance(value_or_tag, str):
            self.Q = value_or_tag  # Set the reservation station tag (string)
