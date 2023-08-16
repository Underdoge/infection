""" This module contains the unit tests for the show_color_picker
    method from the MenuRight class.
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


def test_show_color_picker_healthy(simulation_instance: Simulation) -> None:
    """ This method will test if show_color_picker correctly
        sets the color of the healthy_clr_pkr to the color of
        simulation_instance.healthy_color.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    sim = simulation_instance
    sim.menu_right.healthy_clr_pkr.color = [.5, .5, .5, 1.0]
    sim.menu_right.show_color_picker(
        sim.menu_right.btn_healthy_color, type="healthy")

    assert (
        sim.menu_right.healthy_clr_pkr.color == sim.healthy_color)


def test_show_color_picker_infected(simulation_instance: Simulation) -> None:
    """ This method will test if show_color_picker correctly
        sets the color of the infected_clr_pkr to the color of
        simulation_instance.infected_color.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    sim = simulation_instance
    sim.menu_right.infected_clr_pkr.color = [.5, .5, .5, 1.0]
    sim.menu_right.show_color_picker(
        sim.menu_right.btn_infected_color, type="infected")

    assert (
        sim.menu_right.infected_clr_pkr.color == sim.infected_color)


def test_show_color_picker_recovered(simulation_instance: Simulation) -> None:
    """ This method will test if show_color_picker correctly
        sets the color of the recovered_clr_pkr to the color of
        simulation_instance.recovered_color.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    sim = simulation_instance
    sim.menu_right.recovered_clr_pkr.color = [.5, .5, .5, 1.0]
    sim.menu_right.show_color_picker(
        sim.menu_right.btn_recovered_color, type="recovered")

    assert (
        sim.menu_right.recovered_clr_pkr.color == sim.recovered_color)
