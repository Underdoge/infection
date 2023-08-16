""" This module contains the unit tests for the safe_sum_infected method from
    the Simulation class.
"""
import pytest
from threading import Thread
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


def test_safe_sum_infected_add_one(simulation_instance: Simulation) -> None:
    """ This method will test if safe_sum_infected(1) actually increments the
        simulation_instance.infected counter by one.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation_instance.safe_sum_infected(1)

    assert simulation_instance.infected == 1


def test_safe_sum_infected_remove_one(simulation_instance: Simulation) -> None:
    """ This method will test if safe_sum_infected(-1) actually decreases the
        simulation_instance.infected counter by one.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation_instance.safe_sum_infected(-1)

    assert simulation_instance.infected == -1


def test_safe_sum_infected_add_more_than_one(
        simulation_instance: Simulation) -> None:
    """ This method will test if safe_sum_infected(2) actually increments the
        simulation_instance.infected counter by 2.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation_instance.safe_sum_infected(2)

    assert simulation_instance.infected == 2


def test_safe_sum_infected_remove_more_than_one(
        simulation_instance: Simulation) -> None:
    """ This method will test if safe_sum_infected(-2) actually decreases the
        simulation_instance.infected counter by 2.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    simulation_instance.safe_sum_infected(-2)

    assert simulation_instance.infected == -2


def test_safe_sum_infected_race_condition(
        simulation_instance: Simulation) -> None:
    """ This method will try to simulate a race condition and see if
        safe_sum_infected is able to avoid it as expected.

    Args:
        simulation_instance (Simulation): An instance of the simulation class.
    """
    def increase():
        for _ in range(1_000_000):
            simulation_instance.safe_sum_infected(1)

    def decrease():
        for _ in range(1_000_000):
            simulation_instance.safe_sum_infected(-1)

    thread_a = Thread(target=increase)
    thread_b = Thread(target=decrease)

    thread_a.start()
    thread_b.start()

    thread_a.join()
    thread_b.join()

    assert simulation_instance.infected == 0
