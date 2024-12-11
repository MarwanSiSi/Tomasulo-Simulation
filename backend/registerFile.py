from register import Register, Registers
from typing import Dict, Union


class RegisterFile:
    """Class representing a collection of registers using a hashmap."""
    def __init__(self):
        """
        Initialize a hashmap (dictionary) to store registers by their names.
        Each register is represented by its name, value, and optional station tag (Q).
        """
        self.registers: Dict[str, Register] = {
            e.value: Register(name=e) for e in Registers
        }

    def get_register(self, name: Registers) -> Union[float, str, None]:
        """
        Retrieve the value or reservation station tag of a register by its name.
        :param name: Name of the register.
        :return: The value or station tag of the register, or None if not found.
        """
        if name.value in self.registers:
            return self.registers[name.value].get()
        return None

    def update_register(self, name: Registers, value_or_tag: Union[float, str]) -> bool:
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
            return True
        return False


# Example usage
register_file = RegisterFile()

# Get values or tags
print(register_file.get_register(Registers.R1))  # Output: 0.0 (initial value)
print(register_file.get_register(Registers.R2))  # Output: 0.0 (initial value)

# Update registers
register_file.update_register(Registers.R1, 20.0)
register_file.update_register(Registers.R2, "A1")  # Using a string directly for station tag

# After updates
print(register_file.get_register(Registers.R1))  # Output: 20.0
print(register_file.get_register(Registers.R2))  # Output: "STATION2"

# Try to access a non-existent register
print(register_file.get_register(Registers.R3))  # Output: None (register not found)

# Print all registers
for register_name, register_obj in register_file.registers.items():
    print(f"Register {register_name}: Value = {register_obj.get()}")
