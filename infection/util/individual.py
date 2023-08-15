""" This module defines the Individual abstract class, and its
    HeallthyIndividual and InfectedIndividual subclasses and all of their
    properties and methods.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from infection.simulation import Simulation
    from infection.util.circular_button import CircularButton
    from quads import QuadTree
from infection.decorators.debugging_decorator import debugging_decorator
from quads import BoundingBox
from abc import ABC, abstractmethod
import numpy as np
from random import uniform
import logging

logging.basicConfig(level=10, format="%(threadName)s:%(message)s")
MAX_COOLDOWN = 30
MAX_TIME_INFECTED = 2000


class Individual(ABC):
    """ This is the definition of the Individual abstract class. It inherits
        from the ABC class to make it an abstract class.
    """

    @property
    @abstractmethod
    def status(self) -> str:
        """ String property used to track the infection status of the
            individual.
        """
        pass

    @property
    @abstractmethod
    def simulation(self) -> Simulation:
        """ To store an instance of the simulation class."""
        pass

    @property
    @abstractmethod
    def recovered(self) -> bool:
        """ Boolean property used to track when the individual has recovered
            from an infection.
        """
        pass

    @property
    @abstractmethod
    def time_infected(self) -> int:
        """ Integer property to track how long the individual has been
            infected.
        """
        pass

    @abstractmethod
    def infection(self) -> None:
        """ Abstract method that will control the infection status of the
            individual and decide if it will get infected or if it will
            recover.
        """
        pass

    @abstractmethod
    def recover(self) -> None:
        """ Abstract method that will set the properties when the individual
            recovers from infection
        """
        pass


class HealthyIndividual(Individual):
    """ This is the definition of the HealthyIndividual class. It inherits
        from the Individual abstract class.

    Args:
        simulation (Simulation): Instance of the Simulation class.
        infection_probability (Float): A value from 0 to 1 that
            determines how likely is an individual to get infected.

    Attributes:
        simulation: To store the instance of the simulation class.
        infection_probability: To store the infection_probability.
        recovered: Boolean property used to track when the individual has
            recovered from an infection. False by default. True when it has
            recovered from an infection. An individual that has recovered
            from an infection can no longer get infected.
        time_infected: Integer property that tracks during how many cycles
            the individual has been infected.
        max_time_infected: Integer property that defines how many cycles need
            to pass until the individual recovers.
            Set to MAX_TIME_INFECTED.
        cooldown: Integer property that tracks how many cycles have passed
            after the last infection evaluation to avoid evaluating against
            the same individual multiple times after crossing paths.
        max_cooldown: Integer property that defines how many cycles need
            to pass until the infection evaluations restart.
            Set to MAX_COOLDOWN.
        status: String property that tracks the infection status of the
            individual. "healthy" by default.
    """

    def __init__(self, simulation: Simulation,
                 infection_probability: float, **kwargs):
        super(Individual, self).__init__(**kwargs)
        self._simulation = simulation
        self._infection_probability = infection_probability
        self._recovered = False
        self._time_infected = 0
        self._max_time_infected = MAX_TIME_INFECTED
        self._cooldown = 0
        self._max_cooldown = MAX_COOLDOWN
        self._status = "healthy"

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, status: str) -> None:
        self._status = status

    @property
    def time_infected(self) -> int:
        return self._time_infected

    @time_infected.setter
    def time_infected(self, time_infected: int) -> None:
        self._time_infected = time_infected

    @property
    def max_time_infected(self) -> int:
        return self._max_time_infected

    @property
    def cooldown(self) -> int:
        return self._cooldown

    @cooldown.setter
    def cooldown(self, cooldown: int) -> None:
        self._cooldown = cooldown

    @property
    def max_cooldown(self) -> int:
        return self._max_cooldown

    @property
    def recovered(self) -> int:
        return self._recovered

    @recovered.setter
    def recovered(self, recovered: bool) -> None:
        self._recovered = recovered

    @property
    def infection_probability(self) -> float:
        return self._infection_probability

    @infection_probability.setter
    def infection_probability(self, infection_probability: float) -> None:
        self._infection_probability = infection_probability

    @property
    def simulation(self) -> Simulation:
        return self._simulation

    @simulation.setter
    def simulation(self, simulation: Simulation) -> None:
        self._simulation = simulation

    @debugging_decorator
    def count_infected_neighbors(self, circular_button: CircularButton,
                                 quad_tree: QuadTree) -> int:
        """ Method that searches the quad_tree to find the number of infected
            individuals within the provided radius and returns the count in
            the infected_neighbor_count variable.

        Args:
            circular_button (CircularButton): Instance of the button
                containing the individual.
            quad_tree (QuadTree): A quadtree structure that contains the
                positions of all the individuals in the simulation for fast
                neighbor search.
        Returns:
            infected_neighbor_count (int): The number of infected individuals
                within the provided radius.
        """
        infected_neighbor_count = 0
        infection_radius = circular_button.simulation.individual_size

        """ Get all Points in the quadtree within the individual's radius,
            including the individual itself.
        """
        others = quad_tree.within_bb(
            BoundingBox(circular_button.x - infection_radius,
                        circular_button.y - infection_radius,
                        circular_button.x + infection_radius,
                        circular_button.y + infection_radius))
        if len(others) > 1:
            infected_others = list(filter(lambda x: x.data == "infected",
                                          others))
            """ BoundingBox is a square around the individual's position so
                we still need to filter out some individuals that may be
                outside the infection_radius and the individual itself.
            """
            for infected_other in infected_others:
                distance = circular_button.distance((infected_other.x,
                                                     infected_other.y))
                if distance > 0 and distance <= infection_radius:
                    infected_neighbor_count += 1
        return infected_neighbor_count

    @debugging_decorator
    def evaluate_infection(self, circular_button: CircularButton,
                           quad_tree: QuadTree) -> tuple[int, int]:
        """ Method that calls the count_infected_neighbors method and if
            there's one or more infected neighbors, a formula is used to
            randomly calculate if the individual should get infected based on
            the infection_probability and the number of infected neighbors.

        Args:
            circular_button (CircularButton): Instance of the button
                containing the individual.
            quad_tree (QuadTree): A quadtree structure that contains the
                positions of all the individuals in the simulation for fast
                neighbor search.

        Returns:
            infected (int): 0 if not infected, 1 or more if infected.
            infected_neighbor_count: The number of infected individuals
                within the provided radius.
        """
        infected_neighbor_count = self.count_infected_neighbors(
            circular_button, quad_tree)
        if infected_neighbor_count > 0:
            infected = sum(np.random.choice(
                [0, 1],
                size=infected_neighbor_count,
                p=[1 - self.infection_probability,
                    self.infection_probability]))
            return infected, infected_neighbor_count
        return 0, infected_neighbor_count

    @debugging_decorator
    def sick(self, circular_button: CircularButton) -> None:
        """ Method to set the individual's properties when it gets sick.

        Args:
            circular_button (CircularButton): Instance of the button
                containing the individual.
        """
        self.status = "infected"
        self.simulation.safe_sum_infected(1)
        self.simulation.safe_sum_healthy(-1)
        circular_button.color = self.simulation.infected_color
        circular_button.speed = uniform(0.3, 0.8)
        logging.info("Infected!")

    @debugging_decorator
    def recover(self, circular_button: CircularButton) -> None:
        """ Method to set the individual's properties when it recovers.

        Args:
            circular_button (CircularButton): Instance of the button
                containing the individual.
        """
        self.recovered = True
        self.status = "healthy"
        self.simulation.safe_sum_healthy(1)
        self.simulation.safe_sum_infected(-1)
        circular_button.color = self.simulation.recovered_color
        circular_button.speed = uniform(0.5, 0.9)
        logging.info("Recovered!")

    @debugging_decorator
    def infection(self, circular_button: CircularButton,
                  quad_tree: QuadTree) -> None:
        """ Method that controls if the individual will get infected by
            being around one or more infected individuals in the provided
            quad_tree, or if the individual is now recovered because
            self.max_time_infected cycles have passed after infection.

        Args:
            circular_button (CircularButton): The instance of the button
                containing the individual to change its properties.
            quad_tree (QuadTree): A quadtree structure that contains the
                position of all the individuals in the canvas for fast
                neighbor search.
        """
        if self.recovered:
            pass
        elif self.cooldown > 0:
            self.cooldown -= 1
        elif self.status == "infected":
            self.time_infected += 1
            if self.time_infected == self.max_time_infected:
                self.recover(circular_button)
        else:
            infected, infected_neighbour_count = self.evaluate_infection(
                circular_button, quad_tree)
            if infected_neighbour_count > 0:
                if infected > 0:
                    self.sick(circular_button)
                else:
                    self.cooldown = self.max_cooldown
                    logging.info(f"Contact with {infected_neighbour_count} \
infected neighbors but no infection.")


class InfectedIndividual(Individual):
    """ This is the definition of the InfectedIndividual class. It inherits
    from the Individual abstract class.

    Args:
        simulation (Simulation): Instance of the Simulation class.

    Attributes:
        simulation: To store the instance of the simulation class.
        recovered: Boolean property used to track when the individual has
            recovered from an infection. False by default. True when it has
            recovered from an infection. An individual that has recovered
            from an infection can no longer get infected.
        time_infected: Integer property that tracks during how many cycles
            the individual has been infected.
        max_time_infected: Integer property that defines how many cycles need
            to pass until the individual recovers.
            Set to MAX_TIME_INFECTED.
        status: String property that tracks the infection status of the
            individual. "infected" by default.
    """

    def __init__(self, simulation: Simulation, **kwargs):
        super(Individual, self).__init__(**kwargs)
        self._simulation = simulation
        self._recovered = False
        self._time_infected = 0
        self._max_time_infected = MAX_TIME_INFECTED
        self._status = "infected"

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, status: str) -> None:
        self._status = status

    @property
    def time_infected(self) -> int:
        return self._time_infected

    @time_infected.setter
    def time_infected(self, time_infected: int) -> None:
        self._time_infected = time_infected

    @property
    def max_time_infected(self) -> int:
        return self._max_time_infected

    @property
    def recovered(self) -> bool:
        return self._recovered

    @recovered.setter
    def recovered(self, recovered: bool) -> None:
        self._recovered = recovered

    @property
    def simulation(self) -> Simulation:
        return self._simulation

    @simulation.setter
    def simulation(self, simulation: Simulation) -> None:
        self._simulation = simulation

    @debugging_decorator
    def recover(self, circular_button: CircularButton) -> None:
        """ Method to set the individual's properties when it recovers.

        Args:
            circular_button (CircularButton): Instance of the button
                containing the individual.
        """
        self.recovered = True
        self.status = "healthy"
        self.simulation.safe_sum_healthy(1)
        self.simulation.safe_sum_infected(-1)
        circular_button.color = self.simulation.recovered_color
        circular_button.speed = uniform(0.5, 0.9)
        logging.info("Recovered!")

    @debugging_decorator
    def infection(self, circular_button: CircularButton,
                  quad_tree: QuadTree) -> None:
        """ Method that controls if the individual is now recovered because
            self.max_time_infected cycles have passed after infection.

        Args:
            circular_button (CircularButton): The instance of the button
                containing the individual to change its properties.
            quad_tree (QuadTree): A quadtree structure that contains the
                position of all the individuals in the canvas for fast
                neighbor search. Ignored in the InfectedIndividual class.
        """
        if self.recovered:
            pass
        self.time_infected += 1
        if self.time_infected == self.max_time_infected:
            self.recover(circular_button)
