""" This module contains the unit tests for the evaluate_infection method from
    the Individual class.
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


def test_evaluate_infection_sick(simulation_instance: Simulation) -> None:
    """ This method will test if evaluate_infection() correctly evaluates the
        infection status of a healthy individual with infection probability of
        1.0 when near an infected individual.

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
    healthy_individual = simulation.population[0].individual
    infected, infected_neighbor_count = healthy_individual.evaluate_infection(
        simulation.population[0],
        simulation.quadtree)

    assert infected == 1
    assert infected_neighbor_count == 1


def test_evaluate_infection_healthy(simulation_instance: Simulation) -> None:
    """ This method will test if evaluate_infection() correctly evaluates the
        infection status of a healthy individual with infection probability of
        1.0 when near a healthy individual.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation = simulation_instance
    simulation.menu.lbl_sldr_infection_probability.text = "1.0"
    simulation.add_healthy(1)
    simulation.population[0].pos = (0, 0)
    simulation.add_healthy(1)
    simulation.population[1].pos = (0, simulation.individual_size)
    for circle in simulation.population:
        simulation.quadtree.insert(circle.pos, data=circle.individual.status)
    healthy_individual = simulation.population[0].individual
    infected, infected_neighbor_count = healthy_individual.evaluate_infection(
        simulation.population[0],
        simulation.quadtree)

    assert infected == 0
    assert infected_neighbor_count == 0
