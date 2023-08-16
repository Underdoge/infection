""" This module contains the unit tests for the sick method from
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


def test_sick(simulation_instance: Simulation) -> None:
    """ This method will test if sick() sets a HealthyIndividual's properties
        correctly to make it infected.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation = simulation_instance
    simulation.add_healthy(1)
    simulation.population[0].individual.sick(
        simulation.population[0])
    assert simulation.population[0].individual.status == "infected"
    assert simulation.population[0].color == simulation.infected_color
