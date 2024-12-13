from pprint import pprint
from src.classes.Simulator import Simulator

if __name__ == "__main__":
    PATH = "/home/ahmedgado/SharedDisk/GUC/Tomasulo-Simulation/instructions.txt"

    simulator = Simulator()
    simulator.load_program(PATH)

    while True:
        simulator.update()
        pprint(simulator.register_file)
        pprint(simulator.reservation_stations)
        input()

