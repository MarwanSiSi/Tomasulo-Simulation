from src.enums import InstructionType, Opcode, Registers


class Instruction:
    def __init__(
        self,
        original: str,
        instr_type: InstructionType,
        opcode: Opcode,
        immediate: int | None = None,
        src: Registers | None = None,
        target: Registers | None = None,
        dest: Registers | None = None,
    ):
        self.instr_type = instr_type  # R-type, I-type, or J-type
        self.opcode = opcode  # Opcode from the Opcode enum
        self.immediate = (
            int(immediate) if immediate is not None else None
        )  # Memory immediate (for load/store or label)
        self.src = src  # Source register (Registers enum)
        self.target = target  # Target register (Registers enum)
        self.dest = dest  # Destination register (Registers enum)
        self.original: str = original  # Original instruction string

    def __str__(self):
        return self.original

    def __repr__(self):
        return (
            f"Instruction(type={self.instr_type}, opcode={self.opcode}, "
            f"immediate={self.immediate}, src={self.src}, "
            f"target={self.target}, dest={self.dest})"
        )

    @staticmethod
    def parse_register(register_str):
        """
        Converts a register string to a Registers enum value.
        """
        try:
            return Registers(register_str)
        except ValueError:
            return register_str

    @staticmethod
    def parse_instruction(line, labels, idx):
        """
        Parses a single line of instruction and returns an Instruction object.
        Handles labels as well.
        """
        orignal_line = line
        line = line.strip()

        # Check for a label
        label = None
        if ":" in line:
            parts = line.split(":", 1)
            label = parts[0].strip()
            line = parts[1].strip()
            labels[label] = idx  # Placeholder for now

        parts = list(map(lambda x: x.replace(",", "").strip(), line.split()))
        opcode_str = parts[0]
        operands = parts[1:]

        # Convert the opcode string to an Opcode enum value
        try:
            opcode = Opcode(opcode_str)
        except ValueError:
            raise ValueError(f"Unknown opcode: {opcode_str}")

        # Determine the instruction type and parse operands
        if opcode in {
            Opcode.ADD_D,
            Opcode.SUB_D,
            Opcode.MUL_D,
            Opcode.DIV_D,
            Opcode.ADD_S,
            Opcode.SUB_S,
            Opcode.MUL_S,
            Opcode.DIV_S,
        }:
            instr_type = InstructionType.R_TYPE
            dest, src, target = map(Instruction.parse_register, operands)
            return Instruction(
                orignal_line, instr_type, opcode, src=src, target=target, dest=dest
            )

        elif opcode in {
            Opcode.L_D,
            Opcode.L_S,
            Opcode.LW,
            Opcode.LD,
            Opcode.S_D,
            Opcode.S_S,
            Opcode.SW,
            Opcode.SD,
        }:
            instr_type = InstructionType.I_TYPE
            temp = Instruction.parse_register(operands[1])
            if isinstance(temp, str):
                target, immediate = operands[0], operands[1]
                target = Instruction.parse_register(target)
                return Instruction(
                    orignal_line, instr_type, opcode, target=target, immediate=immediate
                )
            else:
                target, src = operands[0], temp
                target = Instruction.parse_register(target)
                return Instruction(
                    orignal_line, instr_type, opcode, target=target, src=src
                )

        elif opcode in {Opcode.DADDI, Opcode.DSUBI}:
            instr_type = InstructionType.I_TYPE
            dest, src = map(Instruction.parse_register, operands[0:2])
            immediate = operands[2]
            return Instruction(
                orignal_line,
                instr_type,
                opcode,
                src=src,
                dest=dest,
                immediate=immediate,
            )

        elif opcode in {Opcode.BNE, Opcode.BEQ}:
            instr_type = InstructionType.I_TYPE
            src, target, immediate = operands[0], operands[1], operands[2]
            src = Instruction.parse_register(src)
            target = Instruction.parse_register(target)
            immediate = labels[immediate] if immediate in labels else int(immediate)
            return Instruction(
                orignal_line,
                instr_type,
                opcode,
                immediate=immediate,
                src=src,
                target=target,
            )

        else:
            raise ValueError(f"Unhandled opcode: {opcode}")

    @staticmethod
    def parse_instructions_file(filepath) -> list["Instruction"]:
        """
        Reads the instructions text file and parses it into a list of Instruction objects.
        Handles labels and assigns them line numbers.
        """
        instructions = []
        labels: dict[str, int] = {}
        lines = []
        with open(filepath, "r") as file:
            lines = [line.strip() for line in file.readlines() if line.strip() != ""]
            for idx, line in enumerate(lines):
                line = line.strip()
                instruction = Instruction.parse_instruction(line, labels, idx)
                instructions.append(instruction)

        return instructions
