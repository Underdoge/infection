""" This module contains the unit tests for the add_healthy method from
    the Simulation class.
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


def test_add_infected(simulation_instance: Simulation) -> None:
    """ This method will test if add_infected(1) actually increments the
        simulation_instance.infected counter by one.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation_instance.add_infected(1)

    assert simulation_instance.infected == 1


def test_add_infected_more_than_one(simulation_instance: Simulation) -> None:
    """ This method will test if add_infected(2) actually increments the
        simulation_instance.infected counter by 2.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation_instance.add_infected(2)

    assert simulation_instance.infected == 2
