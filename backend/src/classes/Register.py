from src.enums import Registers


class Register:
    def __init__(self, name: Registers, value: int | float = 0.0, Q: str | None = None):
        """
        Initialize a register with a name, value, and optional reservation station tag (Q).
        :param name: The name of the register.
        :param value: The initial value of the register (default is 0.0).
        :param Q: The reservation station tag, which can be a string (default is None).
        """
        self.name = name
        self.value = value
        self.Q = Q  # The reservation station tag can be a string or None.

    def get(self) -> int | float | str:
        """Returns the value or reservation station tag (Q) of the register."""
        if self.name == Registers.R0:
            return 0
        return self.Q if self.Q is not None else self.value

    def update(self, value_or_tag: int | float | str):
        """Updates the register's value or reservation station tag."""
        if self.name == Registers.R0:
            return

        if isinstance(value_or_tag, (int, float)):
            self.value = value_or_tag
            self.Q = None  # Clear Q when directly updating the value
        elif isinstance(value_or_tag, str):
            self.Q = value_or_tag  # Set the reservation station tag (string)
