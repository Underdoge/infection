'''
Canvas stress
=============

This example tests the performance of our Graphics engine by drawing large
numbers of small squares. You should see a black canvas with buttons and a
label at the bottom. Pressing the buttons adds small colored squares to the
canvas.

'''
from classes.menu import Menu
from classes.individual import Individual
import logging
from threading import enumerate, Lock
from concurrent.futures import ThreadPoolExecutor
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from random import randint, uniform
from kivy.vector import Vector
from kivy.clock import Clock

lock = Lock()
logging.basicConfig(level=10, format="%(threadName)s:%(message)s")


class Simulation(App):
    def __init__(self, **kwargs):
        super(Simulation, self).__init__(**kwargs)
        self.thread_pool = ThreadPoolExecutor(
             max_workers=200, thread_name_prefix="Thread-")
        self.threads = len(enumerate())
        self.population = []
        self.healthy = 0
        self.infected = 0

    @property
    def thread_pool(self):
        return self._thread_pool

    @thread_pool.setter
    def thread_pool(self, thread_pool):
        self._thread_pool = thread_pool

    @property
    def infected(self):
        return self._infected

    @infected.setter
    def infected(self, infected_number):
        self._infected = infected_number

    def sum_infected(self, infected_number):
        self.menu.lbl_value_infected.text = str(
            int(self.menu.lbl_value_infected.text) + infected_number)

    @infected.deleter
    def infected(self):
        self._infected = 0

    @property
    def healthy(self):
        return self._healthy

    @healthy.setter
    def healthy(self, healthy_number):
        self._healthy = healthy_number

    def sum_healthy(self, healthy_number):
        self.menu.lbl_value_healthy.text = str(
            int(self.menu.lbl_value_healthy.text) + healthy_number)

    @healthy.deleter
    def healthy(self):
        self._healthy = 0

    @property
    def threads(self):
        return self._threads

    @threads.setter
    def threads(self, threads):
        self._threads = threads

    @threads.deleter
    def threads(self):
        self._threads = 0

    @property
    def population(self):
        return self._population

    @population.setter
    def population(self, population: list):
        self._population = population

    @population.deleter
    def population(self):
        self._population = []

    def reset_population(self, *kwargs):
        self.menu.lbl_value_population.text = "0"
        self.menu.lbl_value_healthy.text = "0"
        self.menu.lbl_value_infected.text = "0"
        self.thread_pool.shutdown()
        self.thread_pool = ThreadPoolExecutor(
             max_workers=200, thread_name_prefix="Thread-")
        del self.threads
        del self.population
        del self.healthy
        del self.infected
        self.layout.canvas.clear()

    def add_healthy(self, count, *largs):
        self.menu.lbl_value_population.text = str(
            int(self.menu.lbl_value_population.text) + count)
        with lock:
            self.healthy += 1
        self.menu.lbl_value_healthy.text = str(self.healthy)
        with self.layout.canvas:
            for x in range(count):
                coordinate = ((uniform(0, self.layout.width - 20),
                               uniform(self.menu.height, self.layout.height)))
                individual = Individual(size=(20, 20),
                                        pos=coordinate,
                                        text="",
                                        color=[0, .3, .7, 1],
                                        simulation=self)
                logging.info(f"New healthy individual with \
{individual.infection_probability} infection probability.")
                individual.speed = uniform(0.5, 0.9)
                individual.direction = Vector(4, 0).rotate(randint(0, 360))
                self.population.append(individual)

    def add_infected(self, count, *largs):
        self.menu.lbl_value_population.text = str(
            int(self.menu.lbl_value_population.text) + count)
        with lock:
            self.infected += 1
        self.menu.lbl_value_infected.text = str(self.infected)
        with self.layout.canvas:
            for x in range(count):
                coordinate = ((uniform(0, self.layout.width - 20),
                               uniform(self.menu.height, self.layout.height)))
                individual = Individual(size=(20, 20),
                                        pos=coordinate,
                                        text="",
                                        color=[.85, .07, .23, 1],
                                        simulation=self)
                logging.info(f"New infected individual with \
{individual.infection_probability} infection probability.")
                individual.state = "infected"
                individual.speed = uniform(0.3, 0.6)
                individual.direction = Vector(4, 0).rotate(randint(0, 360))
                self.population.append(individual)

    def update(self, dt):
        executor = self.thread_pool
        for i in range(0, len(self.population)):
            executor.submit(
                self.population[i].infection(
                    list(filter(
                        lambda x: x.state == "infected",
                        self.population[:i]))+list(
                            filter(
                                lambda x: x.state == "infected",
                                self.population[i+1:])), 10))
        for individual in self.population:
            executor.submit(individual.move(self))
        if len(enumerate()) != self.threads:
            self.threads = len(enumerate())
            logging.info(f"Threads: {self.threads}")

    def build(self):
        self.root = BoxLayout(orientation='vertical')
        self.layout = BoxLayout()
        self.menu = Menu(self, self.layout, size_hint=(1, 0.2))
        self.root.add_widget(self.layout)
        self.root.add_widget(self.menu)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        return self.root
