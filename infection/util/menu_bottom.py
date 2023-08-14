""" The following module is the definition of the MenuBottom class, its
    properties, and its methods.
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider


class MenuBottom(BoxLayout):
    """  This is the definition of the Menu class. It inherits from the
        BoxLayout Kivy class.

    Attributes:
        lbl_infection_probability: Kivy Label to identify the infection
            probability in the menu.
        lbl_sldr_infection_probability: Kivy Label that displays the value
            of the simulation's infection probility.
        sldr_infection_probability: Kivy Slider that allows the user to
            set the infection probability. Its value is bound to the Label
            that displays the value of the simulation's infection probility,
            by the on_value_infection_probability method.
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
        lbl_value_infected: Kivy Label that displays the infected Individual
            count.

    Args:
        simulation (Simulation): An instance of the simulation's class to
        access its methods and control the simulation.
    """

    def __init__(self, simulation, **kwargs):
        super(MenuBottom, self).__init__(**kwargs)
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

    def on_value_infection_probability(self, instance, probality):
        """ Method that updates the text of the infection probability value
            Label to the value of the Slider when it changes.

        Args:
            instance (kivy.uix.slider.Slider): The infection
            probability Slider's instance.
            probality (Float): The value of the new infection probability set
            in the Slider. Goes from 0.0 to 1.0
        """
        self.lbl_sldr_infection_probability.text = str(round(
            probality / 10, 1))
