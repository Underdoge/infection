import pytest
from simulation import Simulation


@pytest.fixture
def simulation_instance():
    simulation = Simulation()
    simulation.build()
    return simulation


def test_safe_sum_infected_add_one(simulation_instance):
    simulation_instance.safe_sum_infected(1)

    assert simulation_instance.infected == 1


def test_safe_sum_infected_remove_one(simulation_instance):
    simulation_instance.safe_sum_infected(-1)

    assert simulation_instance.infected == -1


def test_safe_sum_infected_add_more_than_one(simulation_instance):
    simulation_instance.safe_sum_infected(2)

    assert simulation_instance.infected == 2


def test_add_infected_remove_more_than_one(simulation_instance):
    simulation_instance.safe_sum_infected(-2)

    assert simulation_instance.infected == -2
