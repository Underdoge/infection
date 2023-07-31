import numpy as np
from kivy.properties import (
    NumericProperty, ReferenceListProperty, StringProperty, BooleanProperty
)
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.vector import Vector
from random import uniform
import logging

logging.basicConfig(level=10, format="%(threadName)s:%(message)s")


class Individual(ButtonBehavior, Label):
    state = StringProperty("healthy")
    time_infected = NumericProperty(0)
    recovered = BooleanProperty(False)
    speed = NumericProperty(0)
    direction_x = NumericProperty(0)
    direction_y = NumericProperty(0)
    direction = ReferenceListProperty(direction_x, direction_y)

    def __init__(self, menu, main, **kwargs):
        super(Individual, self).__init__(**kwargs)
        self.menu = menu
        self.main = main
        self._infection_probability = float(
            menu.lbl_sldr_infection_probability.text)

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

    def infection(self, others, radius):
        if self.recovered:
            pass
        if self.state == "infected":
            self.time_infected += 1
            if self.time_infected == 2000:
                logging.info("Recovered!")
                self.recovered = True
                self.state = "healthy"
                self.main.healthy += 1
                self.menu.lbl_value_healthy.text = str(self.main.healthy)
                self.main.infected -= 1
                self.menu.lbl_value_infected.text = str(self.main.infected)
                self.speed = uniform(0.5, 0.9)
        else:
            neighbor_count = 0
            for other in others:
                if other.state == "infected":
                    if self.distance(other.pos) < radius:
                        neighbor_count += 1
            if sum(
                [1 for x in np.random.random(neighbor_count)
                 if x < self.infection_probability]
                 ) > 0:
                logging.info("Infected!")
                self.state = "infected"
                self.main.infected += 1
                self.menu.lbl_value_infected.text = str(self.main.infected)
                self.main.healthy -= 1
                self.menu.lbl_value_healthy.text = str(self.main.healthy)
                self.speed = uniform(0.3, 0.8)
