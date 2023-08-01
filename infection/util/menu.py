from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from functools import partial
from kivy.uix.slider import Slider


class Menu(BoxLayout):
    def __init__(self, main, layout, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.lbl_infection_probability = Label(text='Infection\nProbability:')
        self.lbl_population = Label(text='Population:')
        self.lbl_value_population = Label(text='0')
        self.lbl_healthy = Label(text='Healthy:')
        self.lbl_value_healthy = Label(text='0')
        self.lbl_infected = Label(text='Infected:')
        self.lbl_value_infected = Label(text='0')
        self.lbl_sldr_infection_probability = Label(text='0.2')
        self.sldr_infection_probability = Slider(min=0, max=10, value=2)
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
                                          main.add_healthy, 1))
        self.btn_add_infected = Button(text='    +1\nInfected',
                                       on_press=partial(
                                          main.add_infected, 1))
        self.btn_reset = Button(text='Reset',
                                on_press=partial(
                                    main.reset_population))
        self.add_widget(self.btn_reset)
        self.add_widget(self.btn_add_healthy)
        self.add_widget(self.btn_add_infected)

    def on_value_infection_probability(self, instance, probality):
        self.lbl_sldr_infection_probability.text = str(round(
            probality / 10, 1))
