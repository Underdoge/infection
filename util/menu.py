""" The following module is the definition of the Menu class, its
    properties, and its methods.
"""
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from functools import partial
from kivy.uix.slider import Slider


class Menu(BoxLayout):
    """  This is the definition of the Menu class. It inherits from the
        BoxLayout Kivy class.

    Args:
        BoxLayout (BoxLayout): Kivy layout class that arranges its children
        items in a vertical or horizontal box.
    """
    def __init__(self, simulation, **kwargs):
        """ This method initializes the properties of the Menu class.

        Properties: oh
            lbl_infection_probability: Kivy Label to identify the infection
            probability in the menu.
            lbl_sldr_infection_probability: Kivy Label that displays the value
            of the simulation's infection probility.
            sldr_infection_probability: Kivy Slider that allows the user to
            set the infection probability. Its value is bound to the Label that
            displays the value of the simulation's infection probility, by the
            on_value_infection_probability method.
            lbl_population: Kivy Label to identify the Total Individual
            population count in the menu.
            lbl_value_population: Kivy Label that displays the total Individual
            population count.
            lbl_healthy: Kivy Label to identify the healthy Individual count in
            the menu.
            lbl_value_healthy: Kivy Label that displays the healthy Individual
            count.
            lbl_infected: Kivy Label to identify the infected Individual count
            in the menu.
            lbl_value_healthy: Kivy Label that displays the infected Individual
            count.
            btn_add_healthy: Kivy Button that allows the user to add a healthy
            individual to the simulation.
            btn_add_infected: Kivy Button that allows the user to add an
            infected individual to the simulation.
            btn_reset: Kivy Button that allows the user to reset the
            simulation, removing all healthy and infected individuals.

        Args:
            simulation (Simulation): An instance of the simulation's class to
            access its methods and control the simulation.
        """
        super(Menu, self).__init__(**kwargs)
        self.lbl_infection_probability = Label(text='Infection\nProbability:')
        self.lbl_sldr_infection_probability = Label(text='0.2')
        self.sldr_infection_probability = Slider(min=0, max=10, value=2)
        self.lbl_population = Label(text='Population:')
        self.lbl_value_population = Label(text='0')
        self.lbl_healthy = Label(text='Healthy:')
        self.lbl_value_healthy = Label(text='0')
        self.lbl_infected = Label(text='Infected:')
        self.lbl_value_infected = Label(text='0')
        self.add_widget(self.lbl_population)
        self.add_widget(self.lbl_value_population)
        self.add_widget(self.lbl_healthy)
        self.add_widget(self.lbl_value_healthy)
        self.add_widget(self.lbl_infected)
        self.add_widget(self.lbl_value_infected)
        self.add_widget(self.lbl_infection_probability)
        self.add_widget(self.sldr_infection_probability)
        self.add_widget(self.lbl_sldr_infection_probability)
        self.sldr_infection_probability.bind(
            value=self.on_value_infection_probability)
        self.btn_add_healthy = Button(text='    +1\nHealthy',
                                      on_press=partial(
                                          simulation.add_healthy, 1))
        self.btn_add_infected = Button(text='    +1\nInfected',
                                       on_press=partial(
                                          simulation.add_infected, 1))
        self.btn_reset = Button(text='Reset',
                                on_press=partial(
                                    simulation.reset_population))
        self.add_widget(self.btn_reset)
        self.add_widget(self.btn_add_healthy)
        self.add_widget(self.btn_add_infected)

    def on_value_infection_probability(self, instance, probality):
        """ Method that binds the infection probability Slider with its value
            Label.

        Args:
            instance (kivy.uix.slider.Slider): The infection
            probability Slider's instance.
            probality (Float): The value of the new infection probability set
            in the Slider. Goes from 0.0 to 1.0
        """
        self.lbl_sldr_infection_probability.text = str(round(
            probality / 10, 1))
