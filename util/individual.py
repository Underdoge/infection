""" This module defines the Individual abstract class, and the
    HeallthyIndividual and InfectedIndividual classes and all of their
    properties and methods.
"""
from abc import ABC
import numpy as np
from random import uniform
import logging

logging.basicConfig(level=10, format="%(threadName)s:%(message)s")


class Individual(ABC):
    """ This is the definition of the Individual abstract class. It inherits
        from the ABC class to make it an abstract class.
    """

    def infection(self):
        """ Abstract method that will control the infection status of the
            individual.
        """
        pass


class HealthyIndividual(Individual):
    def __init__(self, simulation, **kwargs):
        """ This method initializes the properties of the HealthyIndividual
            class. It inherits from the Individual class.

        Properties:
            simulation: To store the instance of the simulation class.
            infection_probability: Float property with a value from 0 to 1 that
            determines how likely is an individual to get infected.
            recovered: Boolean property used to track when the individual has
            recovered from an infection. False by default. True when it has
            recovered from an infection. An individual that has recovered
            from an infection can no longer get infected.
            time_infected: Integer property that tracks for how many cycles
            the individual has been infected. After 2000 cycles the individual
            recovers, and can no longer get infected.
            cooldown: Integer property that tracks how many cycles have passed
            after the last infection evaluation. 30 cycles must pass after
            the last evaluation to avoid evaluating against the same individual
            multiple times after crossing paths.
            status: String property that tracks the infection status of the
            individual. "healthy" by default, set to "infected" when the
            individual becomes infected.

        Args:
            simulation: Instance of the simulation class to be able to access
            all the simulation parameters.

        Returns:
            HealthyIndividual: An instance of the HealthyIndividual class.
        """
        super(Individual, self).__init__(**kwargs)
        self.simulation = simulation
        self._infection_probability = float(
            simulation.menu.lbl_sldr_infection_probability.text)
        self._recovered = False
        self._time_infected = 0
        self._cooldown = 0
        self._status = "healthy"

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def time_infected(self):
        return self._time_infected

    @time_infected.setter
    def time_infected(self, time_infected):
        self._time_infected = time_infected

    @property
    def cooldown(self):
        return self._cooldown

    @cooldown.setter
    def cooldown(self, cooldown):
        self._cooldown = cooldown

    @property
    def recovered(self):
        return self._recovered

    @recovered.setter
    def recovered(self, recovered):
        self._recovered = recovered

    @property
    def infection_probability(self):
        return self._infection_probability

    @infection_probability.setter
    def infection_probability(self, probability):
        self._infection_probability = probability

    def infection(self, circular_button, infected_others, radius):
        """ Function that controls if the individual will get infected by
            being around one or more infected individuals in the provided
            infected_others list if they are inside the provided radius,
            or if the individual is now recovered because 2000 cycles
            have passed after infection.
            This calculation is done each cycle. If the individual has
            already recovered then no calculation is done.
            If the individual is during a cool down, meaning the cooldown
            property is greater than zero, then the cooldown property is
            simply decreased by 1.
            If the status of the individual is "infected", then the
            time_infected property is increased by one, and if
            time_infected has reached 2000:
            - the individual is marked as recovered so it can't get reinfected
            - its status is marked as "healthy" again
            - the color of its container button is set to green
            - the simulation's healthy individual count is increased by one and
              the infected individual count is decreased by one, using the
              simulation's safe_sum_healthy and safe_sum_infected
              methods which use "with lock" to avoid a race condition.
            - the speed of its container button is recalculated randomly with
              "uniform" with a value between .5 and .9 which would be faster
              than a button with an infected individual.
            If the status of the individual is "healthy", the provided
            infected_other list is iterated and the infected_neighbor_count
            variable is used to store the number of infected individuals
            within the provided radius. If there's one or more infected
            neighbors, a formula is used to randomly calculate if the
            individual should get infected based on the infection_probability
            and the number of infected neighbors, and the result is stored in
            the "infected" variable.
            If "infected" is greater than 1, the individual gets infected:
            - its status is marked as "infected"
            - the color of its container button is set to red
            - the simulation's healthy individual count is decreased by one and
              the infected individual count is increased by one, using the
              simulation's safe_sum_healthy and safe_sum_infected methods which
              use "with lock" to avoid a race condition.
            - the speed of its container button is recalculated randomly with
              "uniform" with a value between .3 and .8 which would be slower
              than a button with healthy individual.
            If "infected" is not greater than 1 it means the individual was NOT
            infected, and the cooldown property is set to 30.

        Args:
            circular_button (CircularButton): The instance of the button
                containing the individual to change its properties.
            infected_others (List): A list with all the buttons containing
                infected individuals in the simulation.
            radius (Integer): Distance that determines how close a button
                containing a healthy individual needs to be to a button
                containing infected one to get infected.
        """
        if self.recovered:
            pass
        elif self.cooldown > 0:
            self.cooldown -= 1
        elif self.status == "infected":
            self.time_infected += 1
            if self.time_infected == 2000:
                self.recovered = True
                logging.info("Recovered!")
                self.status = "healthy"
                self.simulation.safe_sum_healthy(1)
                self.simulation.safe_sum_infected(-1)
                circular_button.color = [0, .5, 0, 1]
                circular_button.speed = uniform(0.5, 0.9)
        else:
            infected_neighbor_count = 0
            for infected_other in infected_others:
                if circular_button.distance(infected_other.pos) <= radius:
                    infected_neighbor_count += 1
            if infected_neighbor_count > 0:
                infected = sum(
                    [1 for x in np.random.random(
                        infected_neighbor_count
                        ) if x < self.infection_probability])
                if infected > 0:
                    self.status = "infected"
                    logging.info("Infected!")
                    self.simulation.safe_sum_infected(1)
                    self.simulation.safe_sum_healthy(-1)
                    circular_button.color = [.85, .07, .23, 1]
                    circular_button.speed = uniform(0.3, 0.8)
                else:
                    self.cooldown = 30
                    logging.info(f"Contact with {infected_neighbor_count} \
infected neighbors but no infection.")


class InfectedIndividual(Individual):
    def __init__(self, simulation, **kwargs):
        """ This method initializes the properties of the InfectedIndividual
            class. It inherits from the Individual class.

        Properties:
            simulation: To store the instance of the simulation class.
            recovered: Boolean property used to track when the individual has
            recovered from an infection. False by default. True when it has
            recovered from an infection. And individual that has recovered
            from an infection can no longer get infected.
            time_infected: Integer property that tracks for how many cycles
            the individual has been infected. After 2000 cycles the individual
            recovers, and can no longer get infected.
            status: String property that tracks the infection status of the
            individual. "infected" by default, set to "healthy" when the
            individual recovers.

        Args:
            simulation: Instance of the simulation class to be able to access
            all the simulation parameters.

        Returns:
            InfectedIndividual: An instance of the InfectedIndividual class.
        """
        super(Individual, self).__init__(**kwargs)
        self.simulation = simulation
        self._recovered = False
        self._time_infected = 0
        self._status = "infected"

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def time_infected(self):
        return self._time_infected

    @time_infected.setter
    def time_infected(self, time_infected):
        self._time_infected = time_infected

    @property
    def recovered(self):
        return self._recovered

    @recovered.setter
    def recovered(self, recovered):
        self._recovered = recovered

    def infection(self, circular_button, infected_others, radius):
        """ Function that controls if the individual is now recovered because
            2000 cycles have passed after infection.
            This calculation is done each cycle. If the individual has
            already recovered then no calculation is done.
            If the status of the individual is "infected", then the
            time_infected property is increased by one, and if
            time_infected has reached 2000:
            - the individual is marked as recovered so it can't get reinfected
            - its status is marked as "healthy" again
            - the color of its container button is set to green
            - the simulation's healthy individual count is increased by one and
              the infected individual count is decreased by one, using the
              simulation's safe_sum_healthy and safe_sum_infected
              methods which use "with lock" to avoid a race condition.
            - the speed of its container button is recalculated randomly with
              "uniform" with a value between .5 and .9 which would be faster
              than a button with an infected individual.

        Args:
            circular_button (CircularButton): The instance of the button
                containing the individual to change its properties.
            infected_others (List): A list with all the infected individuals in
                                    the simulation. Ignored in the
                                    InfectedIndividual class.
            radius (Integer): Distance that determines how close a healthy
                              individual needs to be to an infected one to get
                              infected. Ignored in the InfectedIndividual
                              class.
        """
        if self.recovered:
            pass
        elif self.status == "infected":
            self.time_infected += 1
            if self.time_infected == 2000:
                self.recovered = True
                logging.info("Recovered!")
                self.status = "healthy"
                self.simulation.safe_sum_healthy(1)
                self.simulation.safe_sum_infected(-1)
                circular_button.color = [0, .5, 0, 1]
                circular_button.speed = uniform(0.5, 0.9)
