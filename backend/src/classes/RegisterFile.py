from src.enums import Registers

from .Register import Register


class RegisterFile:
    """Class representing a collection of registers using a hashmap."""

    def __init__(self, simulator) -> None:
        """
        Initialize a hashmap (dictionary) to store registers by their names.
        Each register is represented by its name, value, and optional station tag (Q).
        """
        self.registers: dict[str, Register] = {
            e.value: Register(name=e) for e in Registers
        }
        self.simulator = simulator

    def __str__(self) -> str:
        """
        Return a string representation of the register file.
        """
        return "\n".join(
            [f"{name}: {register.get()}" for name, register in self.registers.items()]
        )

    def __repr__(self) -> str:
        return self.__str__()

    def get_register(self, name: Registers) -> int | float | str:
        """
        Retrieve the value or reservation station tag of a register by its name.
        :param name: Name of the register.
        :return: The value or station tag of the register.
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

    def update(self) -> None:
        """
        Update all registers in the register file.
        """
        for register in self.registers.values():
            tag, value, valid = self.simulator.cdb.read()
            if not valid:
                continue

            if register.get() == tag:
                register.update(value)
