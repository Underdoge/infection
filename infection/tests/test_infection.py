""" This module contains the unit tests for the infection method from
    the Individual class.
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


def test_infection_sick(simulation_instance):
    """ This method will test if infection() correctly evaluates the infection
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
    for circle in simulation.population:
        simulation.quadtree.insert(circle.pos, data=circle.individual.status)
    simulation.population[0].individual.infection(
        simulation.population[0],
        simulation.quadtree)

    assert simulation.population[0].individual.status == "infected"
    assert simulation.population[0].color == simulation.infected_color


def test_infection_recover(simulation_instance):
    """ This method will test if infection() correctly evaluates the infection
        status of an infected individual and it succesfully recovers when
        max_time_infected has been reached.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation = simulation_instance
    simulation.add_infected(1)
    infected = simulation.population[0].individual
    infected.time_infected = infected.max_time_infected - 1
    for circle in simulation.population:
        simulation.quadtree.insert(circle.pos, data=circle.individual.status)
    simulation.population[0].individual.infection(
        simulation.population[0],
        simulation.quadtree)

    assert simulation.population[0].individual.status == "healthy"
    assert simulation.population[0].color == simulation.recovered_color
