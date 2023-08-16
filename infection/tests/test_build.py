""" This module contains the unit tests for the build method from
    the Simulation class.
"""
import pytest
from infection.simulation import Simulation
from infection.util.menu_bottom import MenuBottom
from infection.util.menu_right import MenuRight
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App


@pytest.fixture
def simulation_instance() -> Simulation:
    """ This is a pytest.fixture method to provide quick access to the class
        that contains the method we are testing.

    Returns:
        simulation (Simulation): An instance of the simulation class.
    """
    simulation = Simulation()
    return simulation


def test_build(simulation_instance: Simulation) -> None:
    """ This method will test if build() correctly initializes all the
        components of the Simulation App instance.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation_instance.build()
    assert isinstance(simulation_instance, App)
    assert isinstance(simulation_instance.root, BoxLayout)
    assert isinstance(simulation_instance.layout, AnchorLayout)
    assert isinstance(simulation_instance.menu_right, MenuRight)
    assert isinstance(simulation_instance.menu_bottom, MenuBottom)
