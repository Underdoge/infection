""" This module contains the unit tests for the reset_population method from
    the Simulation class.
"""
import pytest
from simulation import Simulation


@pytest.fixture
def simulation_instance():
    """ This is a pytest.fixture method to provide quick access to the class
        that contains the method are testing.

    Returns:
        simulation (Simulation): An instance of the simulation class.
    """
    simulation = Simulation()
    simulation.build()
    return simulation


def test_reset_population(simulation_instance):
    """ This method will test if reset_population() actually removes all the
        individuals from the simulation after adding a couple of individuals.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation_instance.add_healthy(1)
    simulation_instance.add_infected(1)
    simulation_instance.reset_population()

    assert simulation_instance.population == []
