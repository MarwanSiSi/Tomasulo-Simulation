from src.enums import Registers
from .Register import Register


class RegisterFile:
    """Class representing a collection of registers using a hashmap."""

    def __init__(self):
        """
        Initialize a hashmap (dictionary) to store registers by their names.
        Each register is represented by its name, value, and optional station tag (Q).
        """
        self.registers: dict[str, Register] = {
            e.value: Register(name=e) for e in Registers
        }

    def get_register(self, name: Registers) -> int | float | str:
        """
        Retrieve the value or reservation station tag of a register by its name.
        :param name: Name of the register.
        :return: The value or station tag of the register, or None if not found.
        """
        if name.value in self.registers:
            return self.registers[name.value].get()
        else:
            raise Exception("Register not found")

    def update_register(self, name: Registers, value_or_tag: int | float | str) -> None:
        """
        Update the value or reservation station tag of a register.
        :param name: Name of the register.
        :param value_or_tag: New value or station tag (as a string).
        :return: True if the register exists and was updated, False otherwise.
        """
        if name.value in self.registers:
            if isinstance(value_or_tag, str):
                # Update with the station tag string
                self.registers[name.value].update(value_or_tag)
            else:
                # Update directly if it's a float value
                self.registers[name.value].update(value_or_tag)
        else:
            raise Exception("Register not found")
