""" This module contains the unit tests for the move method from
    the CircularButton class.
"""
import pytest
from infection.simulation import Simulation


@pytest.fixture
def simulation_instance() -> Simulation:
    """ This is a pytest.fixture method to provide quick access to the class
        that contains the method we are testing.

    Returns:
        simulation (Simulation): An instance of the simulation class.
    """
    simulation = Simulation()
    simulation.build()
    return simulation


def test_move(simulation_instance: Simulation) -> None:
    """ This method will test if move() actually moves an individual in the
        canvas.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation_instance.add_healthy(1)
    original_pos = str(simulation_instance.population[0].pos)
    simulation_instance.population[0].move(simulation_instance)
    new_pos = str(simulation_instance.population[0].pos)

    assert original_pos != new_pos
