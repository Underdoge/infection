""" This module contains the unit tests for the distance method from
    the CircularButton class.
"""
import pytest
from infection.simulation import Simulation


@pytest.fixture
def simulation_instance() -> Simulation:
    """ This is a pytest.fixture method to provide quick access to the class
        that contains the method are testing.

    Returns:
        simulation (Simulation): An instance of the simulation class.
    """
    simulation = Simulation()
    simulation.build()
    return simulation


def test_distance(simulation_instance: Simulation) -> None:
    """ This method will test if distance() correctly measures the distance
        between two individuals in the canvas.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation_instance.add_healthy(1)
    simulation_instance.population[0].pos = (0, 0)
    simulation_instance.add_infected(1)
    simulation_instance.population[1].pos = (0, 10)

    assert simulation_instance.population[0].distance(
        simulation_instance.population[1].pos) == 10
