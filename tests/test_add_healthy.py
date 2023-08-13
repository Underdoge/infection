""" This module contains the unit tests for the add_healthy method from
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


def test_add_healthy(simulation_instance):
    """ This method will test if add_healthy(1) actually increments the
        simulation_instance.healthy counter by one.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation_instance.add_healthy(1)

    assert simulation_instance.healthy == 1


def test_add_healthy_more_than_one(simulation_instance):
    """ This method will test if add_healthy(2) actually increments the
        simulation_instance.healthy counter by 2.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation_instance.add_healthy(2)

    assert simulation_instance.healthy == 2
