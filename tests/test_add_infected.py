import pytest
from infection.util.simulation import Simulation


@pytest.fixture
def simulation_instance():
    simulation = Simulation()
    simulation.build()
    return simulation


def test_add_infected(simulation_instance):
    simulation_instance.add_infected(1)

    assert simulation_instance.infected == 1


def test_add_infected_more_than_one(simulation_instance):
    simulation_instance.add_infected(2)

    assert simulation_instance.infected == 2
