""" This module contains the unit tests for the recover method from
    the Individual class.
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


def test_recover(simulation_instance: Simulation) -> None:
    """ This method will test if recover() sets an InfectedIndividual's
        properties correctly to make it healthy.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation = simulation_instance
    simulation.add_infected(1)
    simulation.population[0].individual.recover(
        simulation.population[0])
    assert simulation.population[0].individual.status == "healthy"
    assert simulation.population[0].color == simulation.recovered_color
