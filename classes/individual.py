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
    direction_x = NumericProperty(0)
    direction_y = NumericProperty(0)
    direction = ReferenceListProperty(direction_x, direction_y)

    def __init__(self, simulation, **kwargs):
        super(Individual, self).__init__(**kwargs)
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
        return np.sqrt((self.pos[0]-coord[0])**2 + (self.pos[1]-coord[1])**2)

    def move(self, window):
        self.pos = (Vector(*self.direction) * self.speed) + self.pos
        if (self.y < window.menu.height) or (self.top > window.root.height):
            self.direction_y *= -1
        if (self.x < 0) or (self.right > window.root.width):
            self.direction_x *= -1

    def infection(self, infected_others, radius):
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
                with lock:
                    self.simulation.healthy += 1
                self.simulation.sum_healthy(1)
                with lock:
                    self.simulation.infected -= 1
                self.simulation.sum_infected(-1)
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
                    with lock:
                        self.simulation.infected += 1
                    self.simulation.sum_infected(1)
                    with lock:
                        self.simulation.healthy -= 1
                    self.simulation.sum_healthy(-1)
                    self.speed = uniform(0.3, 0.8)
                else:
                    logging.info(f"Contact with {infected_neighbor_count} \
infected neighbors but no infection.")
