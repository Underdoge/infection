""" This module defines the CircularButton class and all of its properties
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
import logging

lock = Lock()
logging.basicConfig(level=10, format="%(threadName)s:%(message)s")


class CircularButton(ButtonBehavior, Label):
    """ This is the definition of the CircularButton class. It inherits
        from the ButtonBehavior and Label Kivy classes.

    Args:
        ButtonBehavior: The button behavior class is used to provide a
        Button interface that is easy to manipulate.
        Label: The Label Class is not used, it is only inherited to
        match the Button class definition.
    """

    """ The following direction_x, direction_y, and direction variables are
        Kivy properties required to track the position of the button
        in the canvas. These are the only Kivy properties used because of
        their flexibility and automatic reference. The program will not work
        if regular Python properties are used. For more information visit
        https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty

        direction_x: Kivy NumericProperty that stores the direction in the
        'x' axis. Initialized to 0.
        direction_y: Kivy NumericProperty that stores the direction in the
        'y' axis. Initialized to 0.
        direction: Kivy ReferenceListProperty linked to the direction_x
        and direction_y Kivy properties, to update its value automatically
        whenever either of them changes, and vice versa.
    """
    direction_x = NumericProperty(0)
    direction_y = NumericProperty(0)
    direction = ReferenceListProperty(direction_x, direction_y)

    def __init__(self, individual, simulation, **kwargs):
        """ This method initializes the properties of the CircularButton class.

        Properties:
            size: Tuple property that stores two integers as the size of
            the button in the canvas. (20, 20) by default.
            individual: Stores an instance of a HealthyIndividual or
            InfectedIndividual classes.
            simulation: To store the instance of the simulation class.
            speed: Float property with a value from 0 to 1 that determines
            the speed of the button in the canvas.

        Args:
            individual: Instance of a HealthyIndividual or InfectedIndividual
            classes to control and access its status.
            simulation: Instance of the simulation class to be able to access
            all the simulation parameters.

        Returns:
            CircularButton: An instance of the CircularButton class.
        """
        super(CircularButton, self).__init__(**kwargs)
        self.size = (20, 20)
        self._simulation = simulation
        self._individual = individual
        self._speed = 0

    @property
    def simulation(self):
        return self._simulation

    @simulation.setter
    def simulation(self, simulation):
        self._simulation = simulation

    @property
    def individual(self):
        return self._individual

    @individual.setter
    def individual(self, individual):
        self._individual = individual

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = speed

    def distance(self, coord):
        """ This is a simple formula to calculate the ecludian distance
            between the button's current coordinate (self.pos) and a
            second button's coordinate (coord) in the canvas.

        Args:
            coord (kivy.properties.ObservableReferenceList):
                The position of the second button to measure the distance.

        Returns:
            float: The distance between the two buttons.
        """
        return np.sqrt((self.pos[0]-coord[0])**2 + (self.pos[1]-coord[1])**2)

    def move(self, sim):
        """ Method that moves the button across the canvas one step each
            refresh cycle. If the button is at the edge of the canvas, its
            direction is inverted by multiplying it by -1 to simulate a
            "bounce" against the edge.

        Args:
            sim (simulation): Instance of the main simulation app class
            to access the menu's height and the root widget's height and width
            to check if the button is at the edge of the canvas.
        """
        self.pos = (Vector(*self.direction) * self.speed) + self.pos
        if (self.y < sim.menu.height) or (self.top > sim.root.height):
            self.direction_y *= -1
        if (self.x < 0) or (self.right > sim.root.width):
            self.direction_x *= -1
