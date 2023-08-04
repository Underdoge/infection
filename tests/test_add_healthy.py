import pytest
from infection.util.simulation import Simulation


@pytest.fixture
def simulation_instance():
    simulation = Simulation()
    simulation.build()
    return simulation


def test_add_healthy(simulation_instance):
    simulation_instance.add_healthy(1)

    assert simulation_instance.healthy == 1


def test_add_healthy_more_than_one(simulation_instance):
    simulation_instance.add_healthy(2)

    assert simulation_instance.healthy == 2
