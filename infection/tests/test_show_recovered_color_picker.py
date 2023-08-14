""" This module contains the unit tests for the show_recovered_color_picker
    method from the MenuRight class.
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


def test_show_recovered_color_picker(simulation_instance):
    """ This method will test if show_recovered_color_picker correctly
        sets the color of the recovered_clr_pkr to the color of
        simulation_instance.recovered_color.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    sim = simulation_instance
    sim.menu_right.recovered_clr_pkr.color = [.5, .5, .5, 1.0]
    sim.menu_right.show_recovered_color_picker(
        sim.menu_right.btn_recovered_color)

    assert (
        sim.menu_right.recovered_clr_pkr.color == sim.recovered_color)
