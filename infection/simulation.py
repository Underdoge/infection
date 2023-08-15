""" This module defines the Simulation class and all of its properties
    and methods. This is the main class that controls the simulation.
"""
from __future__ import annotations
from quads import QuadTree
from infection.decorators.debugging_decorator import debugging_decorator
from infection.util.menu_bottom import MenuBottom
from infection.util.menu_right import MenuRight
from infection.util.individual import HealthyIndividual, InfectedIndividual
from infection.util.circular_button import CircularButton
from threading import enumerate, Lock
from concurrent.futures import ThreadPoolExecutor
from random import randint, uniform
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
import logging

lock = Lock()
logging.basicConfig(level=10, format="%(threadName)s:%(message)s")


class Simulation(App):
    """ This is the definition of the Simulation class. It inherits from the
        App Kivy class.

    Attributes:
        thread_pool: A ThreadPoolExecutor instance to spawn new threads
            as required for the simulation, with a maximum of 4 workers.
        threads: Integer that keeps the count of the spawned threads.
        quadtree: A QuadTree structure that contains the positions of all the
            individuals in the simulation for fast neighbor search.
        population: List of all the Individuals in the simulation.
        healthy: Integer that keeps the count of the healthy individuals
            in the simulation.
        infected: Integer that keeps the count of the infected individuals
            in the simulation.
        infection_probability: Float that stores the current infection
            probability value. Initialized to 0.2.
        individual_size: The size of an individual in the canvas. It also
            determines how close a healthy individual needs to be to an
            infected one to get infected. Ignored in the InfectedIndividual
            class. Initialized to Window.size[1] * .035.
        healthy_color: The color of a healthy individual in the canvas.
            Initialized to the rgba value of blue.
        infected_color: The color of an infected individual in the canvas.
            Initialized to the rgba value of red.
        recovered_color: The color of an infected individual in the canvas.
            Initialized to the rgba value of green.
    """

    def __init__(self, **kwargs):
        super(Simulation, self).__init__(**kwargs)
        self._thread_pool = ThreadPoolExecutor(
            max_workers=4)
        self._threads = len(enumerate())
        self._quadtree = QuadTree((0, 0), Window.size[0], Window.size[1])
        self._population = []
        self._healthy = 0
        self._infected = 0
        self._infection_probability = 0.2
        self._individual_size = Window.size[1] * .035
        self._healthy_color = [0, .3, .7, 1]
        self._infected_color = [.85, .07, .23, 1]
        self._recovered_color = [0, .5, 0, 1]

    @property
    def quadtree(self) -> QuadTree:
        return self._quadtree

    @quadtree.setter
    def quadtree(self, quadtree: QuadTree) -> None:
        self._quadtree = quadtree

    @property
    def thread_pool(self) -> ThreadPoolExecutor:
        return self._thread_pool

    @thread_pool.setter
    def thread_pool(self, thread_pool: ThreadPoolExecutor) -> None:
        self._thread_pool = thread_pool

    @property
    def infected(self) -> int:
        return self._infected

    @infected.setter
    def infected(self, infected_number: int) -> None:
        self._infected = infected_number

    @infected.deleter
    def infected(self) -> None:
        self._infected = 0

    @property
    def healthy(self) -> int:
        return self._healthy

    @healthy.setter
    def healthy(self, healthy_number: int) -> None:
        self._healthy = healthy_number

    @healthy.deleter
    def healthy(self) -> None:
        self._healthy = 0

    @property
    def infection_probability(self) -> float:
        return self._infection_probability

    @infection_probability.setter
    def infection_probability(self, infection_probability: float) -> None:
        self._infection_probability = infection_probability

    @property
    def threads(self) -> int:
        return self._threads

    @threads.setter
    def threads(self, threads: int) -> None:
        self._threads = threads

    @threads.deleter
    def threads(self) -> None:
        self._threads = 0

    @property
    def population(self) -> list:
        return self._population

    @population.setter
    def population(self, population: list) -> None:
        self._population = population

    @population.deleter
    def population(self) -> None:
        self._population = []

    @property
    def infection_radius(self) -> int:
        return self._infection_radius

    @infection_radius.setter
    def infection_radius(self, infection_radius: int) -> None:
        self._infection_radius = infection_radius

    @property
    def individual_size(self) -> int:
        return self._individual_size

    @individual_size.setter
    def individual_size(self, individual_size: int) -> None:
        self._individual_size = individual_size

    @property
    def healthy_color(self) -> list:
        return self._healthy_color

    @healthy_color.setter
    def healthy_color(self, healthy_color: list) -> None:
        self._healthy_color = healthy_color

    @property
    def infected_color(self) -> list:
        return self._infected_color

    @infected_color.setter
    def infected_color(self, infected_color: list) -> None:
        self._infected_color = infected_color

    @property
    def recovered_color(self) -> list:
        return self._recovered_color

    @recovered_color.setter
    def recovered_color(self, recovered_color: list) -> None:
        self._recovered_color = recovered_color

    @debugging_decorator
    def safe_sum_healthy(self, healthy_num: int) -> int:
        """ Method that safely increases or decreases the healthy individual
            count, using "with lock" to avoid race condition. It also updates
            the value of the healthy individual count Label in the menu_bottom.

        Args:
            healthy_num (int): The number of healthy individuals to
            increase or decrease.

        Returns:
            self.healthy (int): The final count of healthy individuals.
        """
        with lock:
            self.healthy += healthy_num
            self.menu_bottom.lbl_value_healthy.text = str(
                int(self.menu_bottom.lbl_value_healthy.text) + healthy_num)
        return self.healthy

    @debugging_decorator
    def safe_sum_infected(self, infected_num: int) -> int:
        """ Method that safely increases or decreases the infected individual
            count, using "with lock" to avoid race condition. It also updates
            the value of the infected individual count Label in the menu_bottom

        Args:
            infected_number (int): The number of infected individuals to
            increase or decrease.

        Returns:
            self.infected (int): The final count of infected individuals.
        """
        with lock:
            self.infected += infected_num
            self.menu_bottom.lbl_value_infected.text = str(
                int(
                    self.menu_bottom.lbl_value_infected.text) + infected_num)
        return self.infected

    @debugging_decorator
    def reset_population(self, *largs) -> list:
        """ Method that resets all the simulation's properties to their
            initial states and values.

        Returns:
            self.population (list): An empty list after the population
                was deleted.
        """
        self.menu_bottom.lbl_value_population.text = "0"
        self.menu_bottom.lbl_value_healthy.text = "0"
        self.menu_bottom.lbl_value_infected.text = "0"
        self.thread_pool.shutdown()
        self.thread_pool = ThreadPoolExecutor(
            max_workers=4)
        del self.threads
        del self.population
        del self.healthy
        del self.infected
        self.layout.clear_widgets()
        self.layout.canvas.clear()
        self.layout.add_widget(self.menu_right)
        return self.population

    @debugging_decorator
    def add_healthy(self, number: int, *largs) -> int:
        """ Method that adds new healthy individuals to the simulation. The
            number of individuals added is determined by the provided "number"
            argument.

        Args:
            number (int): The number of healthy individuals to add to the
            simulation.

        Returns:
            self.healthy (int): The final count of healthy individuals.
        """
        self.menu_bottom.lbl_value_population.text = str(
            int(self.menu_bottom.lbl_value_population.text) + number)
        self.safe_sum_healthy(number)
        with self.layout.canvas:
            for x in range(number):
                coordinate = (uniform(
                    0, self.layout.width -
                    self.menu_right.width - self.individual_size),
                    uniform(self.menu_bottom.height, self.layout.height))
                healthy_individual = HealthyIndividual(
                    self, self.infection_probability)
                circular_button = CircularButton(
                    size=(self.individual_size, self.individual_size),
                    pos=coordinate,
                    text="",
                    color=self.healthy_color,
                    simulation=self,
                    individual=healthy_individual)
                logging.info(f"New healthy individual with \
{circular_button.individual.infection_probability} infection probability.")
                circular_button.speed = uniform(0.5, 0.9)
                circular_button.direction = Vector(4, 0).rotate(
                    randint(0, 360))
                self.population.append(circular_button)
                return self.healthy

    @debugging_decorator
    def add_infected(self, number: int, *largs) -> int:
        """ Method that adds new infected individuals to the simulation. The
            number of individuals added is determined by the provided "number"
            argument.

        Args:
            number (int): The number of infected individuals to add to the
            simulation.

        Returns:
            self.infected (int): The final count of infected individuals.
        """
        self.menu_bottom.lbl_value_population.text = str(
            int(self.menu_bottom.lbl_value_population.text) + number)
        self.safe_sum_infected(number)
        with self.layout.canvas:
            for x in range(number):
                coordinate = (uniform(
                    0, self.layout.width -
                    self.menu_right.width - self.individual_size),
                    uniform(self.menu_bottom.height, self.layout.height))
                infected_individual = InfectedIndividual(simulation=self)
                circular_button = CircularButton(
                    size=(self.individual_size, self.individual_size),
                    pos=coordinate,
                    text="",
                    color=self.infected_color,
                    simulation=self,
                    individual=infected_individual)
                logging.info("New infected individual.")
                circular_button.speed = uniform(0.3, 0.6)
                circular_button.direction = Vector(4, 0).rotate(
                    randint(0, 360))
                self.population.append(circular_button)
                return self.infected

    def update(self, dt: float) -> None:
        """ Kivy method used to update the simulation on each cycle.
            It uses the thread pool in self.thread_pool to spawn threads to
            control the infection state and movement of each individual in
            the simulation.
            To control the infection state, the "infection" method of each
            Individual is invoked in a thread, providing it the button
            containing the individual, and a quadtree with the positions of
            all the individuals.
            To control the movement, the "move" method of each Individual is
            invoked in a thread, providing an instance of the main simulation
            so the individual can calculate its position in the canvas and
            determine when it has to change direction.

        Args:
            dt (Float): Internal Kivy property used to update the app on each
            cycle.
        """
        self.quadtree = QuadTree(
            (0, 0), 2 * Window.size[0], 2 * Window.size[1])
        for circle in self.population:
            self.quadtree.insert(circle.pos, data=circle.individual.status)
        executor = self.thread_pool
        for i in range(0, len(self.population)):
            executor.submit(
                self.population[i].individual.infection(
                    self.population[i],
                    self.quadtree))
        for individual in self.population:
            executor.submit(individual.move(self))
        if len(enumerate()) != self.threads:
            self.threads = len(enumerate())
            logging.info(f"Threads: {self.threads}")

    def build(self) -> BoxLayout:
        """ Kivy method that initializes and integrates all the components of
            the Simulation App instance and its graphical components.

        Returns:
            self.root (BoxLayout): An instance of the root Kivy widget that
                contains all the graphical components of the simulation.
        """
        self.root = BoxLayout(orientation='vertical')
        self.layout = AnchorLayout(anchor_x='right', anchor_y='top')
        self.menu_right = MenuRight(self,
                                    orientation='vertical',
                                    size_hint=(.1, .7))
        self.layout.add_widget(self.menu_right)
        self.menu_bottom = MenuBottom(self, size_hint=(1, 0.2))
        self.root.add_widget(self.layout)
        self.root.add_widget(self.menu_bottom)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        return self.root
