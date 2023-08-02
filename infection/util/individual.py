""" This module defines the individual class and all of its properties
    and methods.
"""
import numpy as np
from kivy.properties import (
    NumericProperty, ReferenceListProperty
)
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from threading import Lock
from kivy.vector import Vector
from random import uniform
import logging

lock = Lock()
logging.basicConfig(level=10, format="%(threadName)s:%(message)s")


class Individual(ButtonBehavior, Label):
    """ This is the definition of the individual class. It inherits from the
        ButtonBehavior And Label Kivy classes.

    Args:
        ButtonBehavior: The button behavior class is used to provide a
        circular Button interface that is easy to manipulate.
        Label: The Label Class is not really used, it is  only inherited to
        match the Button class definition.

    Returns:
        Individual: An instance of the Indivudual class.
    """

    """ The following direction_x, direction_y, and direction properties are
        Kivy properties required to track the position of the individual
        in the canvas. These are the only Kivy properties used because of
        their flexibility and automatic reference. The program will not work
        if regular Python properties are used. For more information visit
        https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty
    """
    direction_x = NumericProperty(0)
    direction_y = NumericProperty(0)
    direction = ReferenceListProperty(direction_x, direction_y)

    def __init__(self, simulation, **kwargs):
        """ This method initializes the properties of the Individual class.

        Properties:
            size: Tuple Property that stores two integers to see the size of
            the individual in the canvas. (20, 20) by default.
            simulation: To store the instance of the simulation class.
            infection_robability: Float property with a value from 0 to 1 that
            determines how likely is an individual to get infected.
            recovered: Boolean variable Used to track when the individual has
            recovered from an infection. False by default. True when he has
            recovered from an infection. And individual that has recovered
            from an infection Cano longer get infected.
            speed: Float property with a value from 0 to 1 that determines
            the speed of the individual in the canvas.
            time_infected: Integer property that tracks for how many cycles
            the individual has been infected. After 2000 cycles they individual
            recovers.
            cooldown: Integer property the tracks how many cycles have passed
            after the last infection evaluation, used to avoid multiple
            evaluations with the same individual. 10 cycles must pass after
            the last evaluation to avoid evaluating against the same individual
            multiple times when crossing paths. In the future maybe this could
            be replaced with an individual id to keep track of the last
            evaluated individual.
            state: String property that tracks the infections that is of the
            individual. "Healthy" by default, set to "infected" when there's
            an infection.

        Args:
            simulation: Instance of the simulation class to be able to access
            all the simulation parameters.

        Returns:
            Individual: An instance of the Indivudual class.
        """
        super(Individual, self).__init__(**kwargs)
        self.size = (20, 20)
        self.simulation = simulation
        self.infection_probability = float(
            simulation.menu.lbl_sldr_infection_probability.text)
        self.recovered = False
        self.speed = 0
        self.time_infected = 0
        self.cooldown = 0
        self.state = "healthy"

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

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
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = speed

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

    def distance(self, coord):
        """ This is a simple formula to calculate the ecludian distance
            between the indivdual's current coordinate (self.pos) and a
            second individual's coordinate (coord) in the canvas.

        Args:
            coord (kivy.properties.ObservableReferenceList): 
                The position of the second individual to measure the distance.

        Returns:
            float: The distance between the two individuals.
        """
        return np.sqrt((self.pos[0]-coord[0])**2 + (self.pos[1]-coord[1])**2)

    def move(self, sim):
        """ Method that moves the individual across the canvas one step each
            refresh cycle. If the individual is at the edge of the canvas, its
            direction is inverted by multiplying it by -1 to simulate a
            "bounce" against the edge.

        Args:
            sim (simulation): Instance of the main simulation app class
            to access the menu's height and the root widget's height and width
            to check if the individual is at the edge of the canvas.
        """
        self.pos = (Vector(*self.direction) * self.speed) + self.pos
        if (self.y < sim.menu.height) or (self.top > sim.root.height):
            self.direction_y *= -1
        if (self.x < 0) or (self.right > sim.root.width):
            self.direction_x *= -1

    def infection(self, infected_others, radius):
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
            If the state of the individual is "infected", then the
            time_infected property is increased by one, and if
            time_infected has reached 2000:
            - the individual is marked as recovered so it can't get reinfected
            - its status is marked as "healthy"
            - its color is set back to blue
            - the simulation's healthy individual count is increased by one and
              the infected individual count is decreased by one, using the
              simulation's safe_sum_healthy and safe_sum_infected
              methods which use "with lock" to avoid a race condition.
            - the speed of the individual is recalculated randomly with
              "uniform" with a value between .5 and .9 which would be faster
              than an infected individual.
            If the state of the individual is "healthy", the provided
            infected_other list is iterated and the infected_neighbor_count
            variable is used to store the number of infected individuals
            within the provided radius. If there's one or more infected
            neighbors, a formula is used to randomly calculate if the
            individual should get infected based on the infection_probability
            and the number of infected neighbors, and the result is stored in
            the infected variable.
            If infected is greater than 1 it means the individual was infected:
            - its status is marked as "infected"
            - its color is set to red
            - the simulation's healthy individual count is decreased by one and
              the infected individual count is increased by one, using the
              simulation's safe_sum_healthy and safe_sum_infected methods which
              use "with lock" to avoid a race condition.
            - the speed of the individual is recalculated randomly with
              "uniform" with a value between .3 and .8 which would be slower
              than a healthy individual.
            If infected is not greater than 1 it means the individual was NOT
            infected and the cooldown property is set to 10.

        Args:
            infected_others (List): A list with all the infected individuals in
                                    the simulation.
            radius (Integer): The distance within an infection can occurr.
        """
        if self.recovered:
            pass
        elif self.cooldown > 0:
            self.cooldown -= 1
        elif self.state == "infected":
            self.time_infected += 1
            if self.time_infected == 2000:
                self.recovered = True
                logging.info("Recovered!")
                self.state = "healthy"
                self.color = [0, .5, 0, 1]
                self.simulation.safe_sum_healthy(1)
                self.simulation.safe_sum_infected(-1)
                self.speed = uniform(0.5, 0.9)
        else:
            infected_neighbor_count = 0
            for infected_other in infected_others:
                if self.distance(infected_other.pos) <= radius:
                    infected_neighbor_count += 1
            if infected_neighbor_count > 0:
                infected = sum(
                    [1 for x in np.random.random(
                        infected_neighbor_count
                        ) if x < self.infection_probability])
                if infected > 0:
                    self.state = "infected"
                    logging.info("Infected!")
                    self.color = [.85, .07, .23, 1]
                    self.simulation.safe_sum_infected(1)
                    self.simulation.safe_sum_healthy(-1)
                    self.speed = uniform(0.3, 0.8)
                else:
                    self.cooldown = 10
                    logging.info(f"Contact with {infected_neighbor_count} \
infected neighbors but no infection.")
