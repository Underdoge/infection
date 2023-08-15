""" This module contains the unit tests for the count_infected_neighbors method
    from the Individual class.
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


def test_count_infected_neighbors_two(simulation_instance: Simulation) -> None:
    """ This method will test if count_infected_neighbors() correctly finds
        two infected individuals nearby.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation = simulation_instance
    simulation.add_healthy(1)
    simulation.population[0].pos = (0, 0)
    simulation.add_infected(1)
    simulation.population[1].pos = (0, simulation.individual_size)
    simulation.add_infected(1)
    simulation.population[2].pos = (0, simulation.individual_size)
    for circle in simulation.population:
        simulation.quadtree.insert(circle.pos, data=circle.individual.status)
    healthy_individual = simulation.population[0].individual
    infected_neighbor_count = healthy_individual.count_infected_neighbors(
        simulation.population[0],
        simulation.quadtree)

    assert infected_neighbor_count == 2


def test_count_infected_neighbors_zero(
        simulation_instance: Simulation) -> None:
    """ This method will test if count_infected_neighbors() correctly finds
        no infected individuals when two healthy individuals are nearby.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation = simulation_instance
    simulation.menu_bottom.lbl_sldr_infection_probability.text = "1.0"
    simulation.add_healthy(1)
    simulation.population[0].pos = (0, 0)
    simulation.add_healthy(1)
    simulation.population[1].pos = (0, simulation.individual_size)
    simulation.add_healthy(1)
    simulation.population[2].pos = (0, simulation.individual_size)
    for circle in simulation.population:
        simulation.quadtree.insert(circle.pos, data=circle.individual.status)
    healthy_individual = simulation.population[0].individual
    infected_neighbor_count = healthy_individual.count_infected_neighbors(
        simulation.population[0],
        simulation.quadtree)

    assert infected_neighbor_count == 0
