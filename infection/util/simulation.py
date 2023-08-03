""" This module defines the Simulation class and all of its properties
    and methods. This is the main class that controls the simulation.
"""
from util.menu import Menu
from util.individual import Individual
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
    """ This is the definition of the Individual class. It inherits from the
        App Kivy class.

    Args:
        App (App): The Kivy App class.
    """
    def __init__(self, **kwargs):
        """ This method initializes the properties of the Simulation class.

        Properties:
            thread_pool: A ThreadPoolExecutor instance to spawn new threads
            as required for the simulation, with a maximum of 200 workers.
            threads: Integer that keeps the count of the spawned threads.
            population: List of all the Individuals in the simulation.
            healthy: Integer that keeps account of the healthy individuals
            in the simulation. Initialized to 0.
            infected: Integer that keeps account of the infected individuals
            in the simulation. Initialized to 0.

        Returns:
            Simulation: An instance of the simulation class.
        """
        super(Simulation, self).__init__(**kwargs)
        self.thread_pool = ThreadPoolExecutor(
             max_workers=200)
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

    @infected.deleter
    def infected(self):
        self._infected = 0

    @property
    def healthy(self):
        return self._healthy

    @healthy.setter
    def healthy(self, healthy_number):
        self._healthy = healthy_number

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

    def safe_sum_healthy(self, healthy_number):
        """ Method that safely increases or decreases the healthy individual
            count, using "with lock" to avoid race condition. It also updates
            the value of the healthy individual count Label in the menu.

        Args:
            healthy_number (Integer): The number of healthy individuals to
            increase or decrease.
        """
        with lock:
            self.healthy += healthy_number
            self.menu.lbl_value_healthy.text = str(
                int(self.menu.lbl_value_healthy.text) + healthy_number)

    def safe_sum_infected(self, infected_number):
        """ Method that safely increases or decreases the infected individual
            count, using "with lock" to avoid race condition. It also updates
            the value of the infected individual count Label in the menu.

        Args:
            infected_number (Integer): The number of infected individuals to
            increase or decrease.
        """
        with lock:
            self.infected += infected_number
            self.menu.lbl_value_infected.text = str(
                int(self.menu.lbl_value_infected.text) + infected_number)

    def reset_population(self, *largs):
        """ Method that resets all the simulation's properties to their
            initial states and values.
        """
        self.menu.lbl_value_population.text = "0"
        self.menu.lbl_value_healthy.text = "0"
        self.menu.lbl_value_infected.text = "0"
        self.thread_pool.shutdown()
        self.thread_pool = ThreadPoolExecutor(
             max_workers=200)
        del self.threads
        del self.population
        del self.healthy
        del self.infected
        self.layout.canvas.clear()

    def add_healthy(self, number, *largs):
        """ Method that adds new healthy individuals to the simulation. The
            number of individuals added is determined by the provided "number"
            argument.

        Args:
            number (Integer): The number of healthy individuals to add to the
            simulation.
        """
        self.menu.lbl_value_population.text = str(
            int(self.menu.lbl_value_population.text) + number)
        self.safe_sum_healthy(1)
        with self.layout.canvas:
            for x in range(number):
                coordinate = ((uniform(0, self.layout.width - 20),
                               uniform(self.menu.height, self.layout.height)))
                individual = Individual(pos=coordinate,
                                        text="",
                                        color=[0, .3, .7, 1],
                                        simulation=self)
                logging.info(f"New healthy individual with \
{individual.infection_probability} infection probability.")
                individual.speed = uniform(0.5, 0.9)
                individual.direction = Vector(4, 0).rotate(randint(0, 360))
                self.population.append(individual)

    def add_infected(self, number, *largs):
        """ Method that adds new infected individuals to the simulation. The
            number of individuals added is determined by the provided "number"
            argument.

        Args:
            number (Integer): The number of infected individuals to add to the
            simulation.
        """
        self.menu.lbl_value_population.text = str(
            int(self.menu.lbl_value_population.text) + number)
        self.safe_sum_infected(1)
        with self.layout.canvas:
            for x in range(number):
                coordinate = ((uniform(0, self.layout.width - 20),
                               uniform(self.menu.height, self.layout.height)))
                individual = Individual(pos=coordinate,
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
        """ Kivy method used to update the simulation on each cycle.
            It uses the thread pool in self.thread_pool to spawn threads to
            control the infection state and movement of each individual in
            the simulation.
            To control the infection state, the "infection" method of each
            Individual is invoked in a thread, providing a List of the
            currently infected individuals, and the radius of infection.
            To control the movement, the "move" method of each Individual is
            invoked in a thread, providing an instance of the main simulation
            so the individual can calculate its position in the canvas and
            determine when it has to change direction.

        Args:
            dt (Float): Internal Kivy property used to update the app on each
            cycle.
        """
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
        """ Kivy method that initializes and integrates all the components of
            the Simulation App instance and its graphical components.

        Returns:
            root (BoxLayout): An instance of the root Kivy widget that
            contains all the graphical components of the simulation.
        """
        self.root = BoxLayout(orientation='vertical')
        self.layout = BoxLayout()
        self.menu = Menu(self, size_hint=(1, 0.2))
        self.root.add_widget(self.layout)
        self.root.add_widget(self.menu)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        return self.root
