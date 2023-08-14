""" This module contains the unit tests for the on_value_infection_probability
    method from the MenuBottom class.
"""
import pytest
from infection.simulation import Simulation


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


def test_on_value_infection_probability(simulation_instance):
    """ This method will test if on_value_infection_probability correctly
        updates the text of the infection probability value Label to the
        value of the Slider when it changes.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation = simulation_instance
    simulation.menu.sldr_infection_probability.value = 10

    assert simulation.menu.lbl_sldr_infection_probability.text == "1.0"
