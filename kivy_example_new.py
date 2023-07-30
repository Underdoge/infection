'''
Canvas stress
=============

This example tests the performance of our Graphics engine by drawing large
numbers of small squares. You should see a black canvas with buttons and a
label at the bottom. Pressing the buttons adds small colored squares to the
canvas.

'''
import numpy as np
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from random import random, randint, uniform
from functools import partial
from kivy.properties import (
    NumericProperty, ReferenceListProperty, StringProperty, BooleanProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.slider import Slider

logging.basicConfig(level=10, format="%(threadName)s:%(message)s")


class Individual(ButtonBehavior, Label):

    state = StringProperty("healthy")
    time_infected = NumericProperty(0)
    recovered = BooleanProperty(False)
    speed = NumericProperty(0)
    direction_x = NumericProperty(0)
    direction_y = NumericProperty(0)
    direction = ReferenceListProperty(direction_x, direction_y)

    def distance(self, coord):
        return np.sqrt((self.pos[0]-coord[0])**2 + (self.pos[1]-coord[1])**2)

    def move(self, window):
        self.pos = (Vector(*self.direction) * self.speed) + self.pos
        if (self.y < window.menu.height) or (self.top > window.root.height):
            self.direction_y *= -1
        if (self.x < 0) or (self.right > window.root.width):
            self.direction_x *= -1

    def infection(self, others, radius, probability):
        # if self.recovered:
        # pass
        if self.state == "infected":
            self.time_infected += 1
            if self.time_infected == 2000:
                logging.info("Recovered!")
                self.state = "healthy"
                self.speed = uniform(0.5, 0.9)
                self.recovered = True
        else:
            neighbor_count = 0
            for other in others:
                if other.state == "infected":
                    if self.distance(other.pos) < radius:
                        neighbor_count += 1
            if sum(
                [1 for x in np.random.random(neighbor_count)
                 if x < probability]
                 ) > 0:
                logging.info("Infected!")
                self.state = "infected"
                self.speed = uniform(0.3, 0.8)


class Menu(BoxLayout):
    def __init__(self, main, layout, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.lbl_infection_probability = Label(text='Infection\nProbability:')
        self.lbl_population = Label(text='Population:')
        self.lbl_value_population = Label(text='0')
        self.lbl_sldr_infection_probability = Label(text='0.5')
        self.sldr_infection_probability = Slider(min=0, max=10, value=5)
        self.add_widget(self.lbl_population)
        self.add_widget(self.lbl_value_population)
        self.add_widget(self.lbl_infection_probability)
        self.add_widget(self.sldr_infection_probability)
        self.add_widget(self.lbl_sldr_infection_probability)
        self.sldr_infection_probability.bind(
            value=self.on_value_infection_probability)
        self.btn_add_healthy = Button(text='+ 1 Healthy\nsubject',
                                      on_press=partial(
                                          main.add_healthy,
                                          self,
                                          layout, 1))
        self.btn_add_infected = Button(text='+ 1 Infected\nsubject',
                                       on_press=partial(
                                          main.add_infected,
                                          self,
                                          layout, 1))
        self.btn_reset = Button(text='Reset',
                                on_press=partial(
                                    main.reset_population,
                                    self, layout))
        self.add_widget(self.btn_reset)
        self.add_widget(self.btn_add_healthy)
        self.add_widget(self.btn_add_infected)

    def on_value_infection_probability(self, instance, probality):
        self.lbl_sldr_infection_probability.text = str(round(
            probality / 10, 1))


class MainWindow(App):
    @property
    def population(self):
        return self._population

    @population.setter
    def population(self, population: list):
        self._population = population

    @population.deleter
    def population(self):
        self.population = []

    def reset_population(self, lbl, wid, *largs):
        lbl.lbl_value_population.text = "0"
        del self.population
        print(f"population: {len(self.population)}")
        wid.canvas.clear()

    def pause_population(self, secs, *largs):
        Clock.usleep(secs)

    def add_healthy(self, lbl, wid, count, *largs):
        lbl.lbl_value_population.text = str(int(
            lbl.lbl_value_population.text) + count)
        with wid.canvas:
            for x in range(count):
                # Color(r(), 1, 1, mode='hsv')
                individual = Individual(size=(20, 20),
                                        pos=((random() * wid.width + wid.x-10,
                                             random() * wid.height + wid.y-10)
                                             ),
                                        text="")
                individual.speed = uniform(0.5, 0.9)
                individual.direction = Vector(4, 0).rotate(randint(0, 360))
                self.population.append(individual)
                print(f"population: {len(self.population)}")

    def add_infected(self, lbl, wid, count, *largs):
        lbl.lbl_value_population.text = str(
            int(lbl.lbl_value_population.text) + count)
        with wid.canvas:
            for x in range(count):
                # Color(r(), 1, 1, mode='hsv')
                individual = Individual(size=(20, 20),
                                        pos=((random() * wid.width + wid.x-10,
                                             random() * wid.height + wid.y-10)
                                             ),
                                        text="")
                individual.state = "infected"
                individual.speed = uniform(0.3, 0.8)
                individual.direction = Vector(4, 0).rotate(randint(0, 360))
                self.population.append(individual)
                logging.info(f"Population: {len(self.population)}")

    def update(self, dt):
        with ThreadPoolExecutor(
             max_workers=50, thread_name_prefix="Thread-") as executor:
            for i in range(0, len(self.population)):
                executor.submit(self.population[i].infection(
                    self.population[:i]+self.population[i+1:],
                    10, .5))
            for individual in self.population:
                executor.submit(individual.move(self))
            logging.info(f"Threads: {len(threading.enumerate())}")

    def build(self):
        self.population = []
        self.root = BoxLayout(orientation='vertical')
        layout = BoxLayout(size_hint=(1, None), height=700)
        self.menu = Menu(self, layout)
        self.root.add_widget(layout)
        self.root.add_widget(self.menu)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        return self.root


if __name__ == '__main__':
    MainWindow().run()
