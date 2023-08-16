""" This module contains the unit tests for the save_color method from the
    MenuRight class.
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


def test_save_color_healthy(simulation_instance: Simulation) -> None:
    """ This method will test if save_color correctly sets
        simulation_instance.healthy_color to the color of healthy_clr_pkr.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation_instance.menu_right.healthy_clr_pkr.color = [.5, .5, .5, 1.0]
    simulation_instance.menu_right.save_color(
        simulation_instance.menu_right.btn_save_healthy_color, 'healthy')

    assert simulation_instance.healthy_color == [.5, .5, .5, 1.0]


def test_save_color_infected(simulation_instance: Simulation) -> None:
    """ This method will test if save_color correctly sets
        simulation_instance.infected_color to the color of infected_clr_pkr.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation_instance.menu_right.infected_clr_pkr.color = [.5, .5, .5, 1.0]
    simulation_instance.menu_right.save_color(
        simulation_instance.menu_right.btn_save_infected_color, 'infected')

    assert simulation_instance.infected_color == [.5, .5, .5, 1.0]


def test_save_color_recovered(simulation_instance: Simulation) -> None:
    """ This method will test if save_color correctly sets
        simulation_instance.recovered_color to the color of recovered_clr_pkr.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation_instance.menu_right.recovered_clr_pkr.color = [.5, .5, .5, 1.0]
    simulation_instance.menu_right.save_color(
        simulation_instance.menu_right.btn_save_recovered_color, 'recovered')

    assert simulation_instance.recovered_color == [.5, .5, .5, 1.0]
