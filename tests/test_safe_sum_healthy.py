import pytest
from infection.util.simulation import Simulation


@pytest.fixture
def simulation_instance():
    simulation = Simulation()
    simulation.build()
    return simulation


def test_safe_sum_healthy_add_one(simulation_instance):
    simulation_instance.safe_sum_healthy(1)

    assert simulation_instance.healthy == 1


def test_safe_sum_healthy_remove_one(simulation_instance):
    simulation_instance.safe_sum_healthy(-1)

    assert simulation_instance.healthy == -1


def test_safe_sum_healthy_add_more_than_one(simulation_instance):
    simulation_instance.safe_sum_healthy(2)

    assert simulation_instance.healthy == 2


def test_add_healthy_remove_more_than_one(simulation_instance):
    simulation_instance.safe_sum_healthy(-2)

    assert simulation_instance.healthy == -2
