from pprint import pprint
from src.classes.Instruction import Instruction


if __name__ == "__main__":
    pprint(
        Instruction.parse_instructions_file(
            "/home/ahmedgado/SharedDisk/GUC/Tomasulo-Simulation/instructions.txt"
        )
    )
