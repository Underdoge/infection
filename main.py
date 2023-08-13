""" This is the main module where the simulation class is loaded
    and the Simulation App is launched.
"""
from infection.simulation import Simulation


if __name__ == '__main__':
    Simulation(title="Infection").run()
