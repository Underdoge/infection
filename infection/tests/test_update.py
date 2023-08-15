""" This module contains the unit tests for the update method from
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


def test_update_position(simulation_instance: Simulation) -> None:
    """ This method will test if update() correctly updates the position of the
        individuals in the canvas.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation_instance.add_healthy(1)
    original_pos = str(simulation_instance.population[0].pos)
    simulation_instance.update(1.8)
    new_pos = str(simulation_instance.population[0].pos)

    assert original_pos != new_pos


def test_update_infection_sick(simulation_instance: Simulation) -> None:
    """ This method will test if update() correctly updates the infection
        status of a healthy individual with infection probability of 1.0
        when near an infected individual and makes it sick.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation = simulation_instance
    simulation.menu.lbl_sldr_infection_probability.text = "1.0"
    simulation.add_healthy(1)
    simulation.population[0].pos = (0, 0)
    simulation.add_infected(1)
    simulation.population[1].pos = (0, simulation.individual_size)
    simulation.update(1.7)

    assert simulation.population[0].individual.status == "infected"
    assert simulation.population[0].color == simulation.infected_color


def test_update_infection_recover(simulation_instance: Simulation) -> None:
    """ This method will test if update() correctly updates the infection
        status of an infected individual and it succesfully recovers when
        max_time_infected has been reached.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation = simulation_instance
    simulation.add_infected(1)
    infected = simulation.population[0].individual
    infected.time_infected = infected.max_time_infected - 1
    simulation.update(1.7)

    assert simulation.population[0].individual.status == "healthy"
    assert simulation.population[0].color == simulation.recovered_color
