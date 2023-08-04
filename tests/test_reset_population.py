import pytest
from simulation import Simulation


@pytest.fixture
def simulation_instance():
    simulation = Simulation()
    simulation.build()
    return simulation


def test_reset_population(simulation_instance):
    simulation_instance.add_healthy(1)
    simulation_instance.reset_population()

    assert simulation_instance.population == []
