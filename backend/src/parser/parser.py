from enum import Enum

class InstructionType(Enum):
    R_TYPE = "R_TYPE"
    I_TYPE = "I_TYPE"
    J_TYPE = "J_TYPE"

class Opcode(Enum):
    DADDI = "DADDI"
    DSUBI = "DSUBI"
    ADD_D = "ADD.D"
    ADD_S = "ADD.S"
    SUB_D = "SUB.D"
    SUB_S = "SUB.S"
    MUL_D = "MUL.D"
    MUL_S = "MUL.S"
    DIV_D = "DIV.D"
    DIV_S = "DIV.S"
    LW = "LW"
    LD = "LD"
    L_S = "L.S"
    L_D = "L.D"
    SW = "SW"
    SD = "SD"
    S_S = "S.S"
    S_D = "S.D"
    BNE = "BNE"
    BEQ = "BEQ"

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

class Instruction:
    def __init__(self, instr_type, opcode: Opcode, immediate=None, src=None, target=None, dest=None):
        self.type = instr_type          # R-type, I-type, or J-type
        self.opcode = opcode            # Opcode from the Opcode enum
        self.immediate = immediate      # Memory immediate (for load/store or label)
        self.src = src                  # Source register (Registers enum)
        self.target = target            # Target register (Registers enum)
        self.dest = dest                # Destination register (Registers enum)

    def __repr__(self):
        return (f"Instruction(type={self.type}, opcode={self.opcode}, "
                f"immediate={self.immediate}, src={self.src}, "
                f"target={self.target}, dest={self.dest})")

def parse_register(register_str):
    """
    Converts a register string to a Registers enum value.
    """
    try:
        return Registers(register_str)
    except ValueError:
        return register_str

def parse_instruction(line, labels, idx):
    """
    Parses a single line of instruction and returns an Instruction object.
    Handles labels as well.
    """
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
    if opcode in {Opcode.ADD_D, Opcode.SUB_D, Opcode.MUL_D, Opcode.DIV_D, 
                  Opcode.ADD_S, Opcode.SUB_S, Opcode.MUL_S, Opcode.DIV_S}:
        instr_type = InstructionType.R_TYPE
        dest, src, target = map(parse_register, operands)
        return Instruction(instr_type, opcode, src=src, target=target, dest=dest)

    elif opcode in {Opcode.L_D, Opcode.L_S, Opcode.LW, Opcode.LD, Opcode.S_D, 
                    Opcode.S_S, Opcode.SW, Opcode.SD}:
        instr_type = InstructionType.I_TYPE
        temp = parse_register(operands[1])
        if isinstance(temp, str):
            target, immediate = operands[0], operands[1]
            target = parse_register(target)
            return Instruction(instr_type, opcode, target=target, immediate=immediate)
        else:
            target, src = operands[0], temp
            target = parse_register(target)
            return Instruction(instr_type, opcode, target=target, src=src)
        
    elif opcode in {Opcode.DADDI, Opcode.DSUBI}:
        instr_type = InstructionType.I_TYPE
        dest, src, immediate = operands
        return Instruction(instr_type, opcode, src=src, dest=dest, immediate=immediate)
    
    elif opcode in {Opcode.BNE, Opcode.BEQ}:
        instr_type = InstructionType.I_TYPE
        src, target, immediate = operands[0], operands[1], operands[2]
        src = parse_register(src)
        target = parse_register(target)
        immediate = labels[immediate] if immediate in labels else int(immediate)
        return Instruction(instr_type, opcode, immediate=immediate, src=src, target=target)

    else:
        raise ValueError(f"Unhandled opcode: {opcode}")

def parse_instructions_file(filepath):
    """
    Reads the instructions text file and parses it into a list of Instruction objects.
    Handles labels and assigns them line numbers.
    """
    instructions = []
    labels = {}
    lines = []
    with open(filepath, "r") as file:
        lines = [line.strip() for line in file.readlines() if line.strip() != ""]
        for (idx, line) in enumerate(lines):
            line = line.strip()
            instruction = parse_instruction(line, labels, idx)
            instructions.append(instruction)

    return instructions

if __name__ == "__main__":
    filepath = "instructions.txt"
    instructions = parse_instructions_file(filepath)
    for instr in instructions:
        print(instr)
