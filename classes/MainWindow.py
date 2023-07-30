'''
Canvas stress
=============

This example tests the performance of our Graphics engine by drawing large
numbers of small squares. You should see a black canvas with buttons and a
label at the bottom. Pressing the buttons adds small colored squares to the
canvas.

'''
from classes.Menu import Menu
from classes.Individual import Individual
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from random import random, randint, uniform
from kivy.vector import Vector
from kivy.clock import Clock

logging.basicConfig(level=10, format="%(threadName)s:%(message)s")


class MainWindow(App):
    @property
    def infected(self):
        return self._infected

    @infected.setter
    def infected(self, num):
        self._infected = num

    @infected.deleter
    def infected(self):
        self._infected = 0

    @property
    def healthy(self):
        return self._healthy

    @healthy.setter
    def healthy(self, num):
        self._healthy = num

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

    def reset_population(self, menu, wid, *largs):
        menu.lbl_value_population.text = "0"
        menu.lbl_value_healthy.text = "0"
        menu.lbl_value_infected.text = "0"
        del self.population
        del self.healthy
        del self.infected
        print(f"population: {len(self.population)}")
        wid.canvas.clear()

    def add_healthy(self, menu, wid, count, *largs):
        menu.lbl_value_population.text = str(int(
            menu.lbl_value_population.text) + count)
        self.healthy += 1
        menu.lbl_value_healthy.text = str(self.healthy)
        with wid.canvas:
            for x in range(count):
                coordinate = ((random() * wid.width + wid.x,
                               random() * wid.height + wid.y))
                individual = Individual(size=(20, 20),
                                        pos=coordinate,
                                        text="",
                                        menu=menu,
                                        main=self)
                logging.info(f"New healthy individual at: {coordinate} with \
{individual.infection_probability} infection probability.")
                individual.speed = uniform(0.5, 0.9)
                individual.direction = Vector(4, 0).rotate(randint(0, 360))
                self.population.append(individual)
                print(f"population: {len(self.population)}")

    def add_infected(self, menu, wid, count, *largs):
        menu.lbl_value_population.text = str(
            int(menu.lbl_value_population.text) + count)
        self.infected += 1
        menu.lbl_value_infected.text = str(self.infected)
        with wid.canvas:
            for x in range(count):
                coordinate = ((random() * wid.width + wid.x,
                               random() * wid.height + wid.y))
                individual = Individual(size=(20, 20),
                                        pos=coordinate,
                                        text="",
                                        menu=menu,
                                        main=self)
                logging.info(f"New infected individual at: {coordinate} with \
{individual.infection_probability} infection probability.")
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
                    self.population[:i]+self.population[i+1:], 10))
            for individual in self.population:
                executor.submit(individual.move(self))
            if len(threading.enumerate()) != self.threads:
                self.threads = len(threading.enumerate())
                logging.info(f"Threads: {self.threads}")

    def build(self):
        self.threads = len(threading.enumerate())
        self.population = []
        self.healthy = 0
        self.infected = 0
        self.root = BoxLayout(orientation='vertical')
        self.layout = BoxLayout()
        self.menu = Menu(self, self.layout, size_hint=(1, 0.2))
        self.root.add_widget(self.layout)
        self.root.add_widget(self.menu)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        return self.root
