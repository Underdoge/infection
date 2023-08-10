""" The following module is the definition of the MenuRight class, its
    properties, and its methods.
"""
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from functools import partial
from kivy.uix.popup import Popup
from kivy.uix.colorpicker import ColorPicker


class MenuRight(BoxLayout):
    """ This is the definition of the MenuRight class. It inherits from the
        BoxLayout Kivy class.

    Args:
        simulation (Simulation): Instance of the Simulation class.

    Attributes:
        simulation: Here we store the instance of the Simulation class.
        btn_add_healthy: Kivy Button that allows the user to add a healthy
            individual to the simulation.
        btn_add_infected: Kivy Button that allows the user to add an
            infected individual to the simulation.
        btn_reset: Kivy Button that allows the user to reset the
            simulation, removing all healthy and infected individuals.
        btn_healthy_color: Kivy Button that shows the
            popup_healthy_color_picker.
        btn_cancel_healthy_color: Kivy Button that closes the
            popup_healthy_color_picker.
        btn_save_healthy_color: Kivy Button to save the Healthy Individual
            color.
        healthy_clr_pkr: Kivy ColorPicker to allow the user to change the
            color of the Healthy Individual.
        popup_healthy_color_picker: Kivy Popup widget that contains the
            healthy_clr_pkr, btn_cancel_healthy_color and
            btn_save_healthy_color widgets.
        btn_infected_color: Kivy Button that shows the
            popup_infected_color_picker.
        btn_cancel_infected_color: Kivy Button that closes the
            popup_infected_color_picker.
        btn_save_infected_color: Kivy Button to save the Infected Individual
            color.
        infected_clr_pkr: Kivy ColorPicker to allow the user to change the
            color of the Infected Individual.
        popup_infected_color_picker: Kivy Popup widget that contains the
            infected_clr_pkr, btn_cancel_infected_color and
            btn_save_infected_color widgets.
        btn_recovered_color: Kivy Button that shows the
            popup_recovered_color_picker.
        btn_cancel_recovered_color: Kivy Button that closes the
            popup_recovered_color_picker.
        btn_save_recovered_color: Kivy Button to save the Recovered Individual
            color.
        recovered_clr_pkr: Kivy ColorPicker to allow the user to change
            the color of the Recovered Individual.
        popup_recovered_color_picker: Kivy Popup widget that contains the
            recovered_clr_pkr, btn_cancel_recovered_color and
            btn_save_recovered_color widgets.
    """

    def __init__(self, simulation, **kwargs):
        super(MenuRight, self).__init__(**kwargs)
        self.simulation = simulation
        self.btn_add_healthy = Button(text='    +1\nHealthy',
                                      on_press=partial(
                                          simulation.add_healthy, 1))
        self.btn_add_infected = Button(text='    +1\nInfected',
                                       on_press=partial(
                                           simulation.add_infected, 1))
        self.btn_reset = Button(text='Reset',
                                on_press=simulation.reset_population)
        self.btn_healthy_color = Button(text='Healthy\n  Color',
                                        on_press=partial(
                                            self.show_healthy_color_picker))
        self.btn_infected_color = Button(text='Infected\n   Color',
                                         on_press=partial(
                                             self.show_infected_color_picker))
        self.btn_recovered_color = Button(
            text='Recovered\n     Color',
            on_press=partial(
                self.show_recovered_color_picker))
        self.btn_cancel_healthy_color = Button(text='Cancel',
                                               on_press=partial(
                                                   self.cancel_color,
                                                   type="healthy"),
                                               size_hint=(.2, .1),
                                               pos_hint={'x': .6, 'y': 0})
        self.healthy_clr_pkr = ColorPicker()
        self.btn_save_healthy_color = Button(text='Save',
                                             on_press=partial(
                                                 self.save_color,
                                                 type="healthy"),
                                             size_hint=(.2, .1),
                                             pos_hint={'x': .8, 'y': 0})
        self.popup_healthy_color_picker = Popup(
            title='Healthy Individual Color',
            content=self.healthy_clr_pkr,
            size_hint=(.5, .7))
        self.healthy_clr_pkr.add_widget(self.btn_save_healthy_color)
        self.healthy_clr_pkr.add_widget(self.btn_cancel_healthy_color)
        self.infected_clr_pkr = ColorPicker()
        self.btn_cancel_infected_color = Button(text='Cancel',
                                                on_press=partial(
                                                    self.cancel_color,
                                                    type="infected"),
                                                size_hint=(.2, .1),
                                                pos_hint={'x': .6, 'y': 0})
        self.btn_save_infected_color = Button(text='Save',
                                              on_press=partial(
                                                  self.save_color,
                                                  type="infected"),
                                              size_hint=(.2, .1),
                                              pos_hint={'x': .8, 'y': 0})
        self.popup_infected_color_picker = Popup(
            title='Infected Individual Color',
            content=self.infected_clr_pkr,
            size_hint=(.5, .7))
        self.infected_clr_pkr.add_widget(self.btn_cancel_infected_color)
        self.infected_clr_pkr.add_widget(self.btn_save_infected_color)
        self.recovered_clr_pkr = ColorPicker()
        self.btn_cancel_recovered_color = Button(text='Cancel',
                                                 on_press=partial(
                                                     self.cancel_color,
                                                     type="recovered"),
                                                 size_hint=(.2, .1),
                                                 pos_hint={'x': .6, 'y': 0})
        self.btn_save_recovered_color = Button(text='Save',
                                               on_press=partial(
                                                   self.save_color,
                                                   type="recovered"),
                                               size_hint=(.2, .1),
                                               pos_hint={'x': .8, 'y': 0})
        self.popup_recovered_color_picker = Popup(
            title='Recovered Individual Color',
            content=self.recovered_clr_pkr,
            size_hint=(.5, .7))
        self.recovered_clr_pkr.add_widget(self.btn_cancel_recovered_color)
        self.recovered_clr_pkr.add_widget(self.btn_save_recovered_color)
        self.add_widget(self.btn_add_healthy)
        self.add_widget(self.btn_add_infected)
        self.add_widget(self.btn_healthy_color)
        self.add_widget(self.btn_infected_color)
        self.add_widget(self.btn_recovered_color)
        self.add_widget(self.btn_reset)

    def show_healthy_color_picker(self, instance):
        """ Method that opens the popup_healthy_color_picker popup.

        Args:
            instance (kivy.uix.button.Button): The clicked Button's
                instance.
        """
        self.healthy_clr_pkr.color = self.simulation.healthy_color
        self.popup_healthy_color_picker.open()

    def show_infected_color_picker(self, instance):
        """ Method that opens the popup_infected_color_picker popup.

        Args:
            instance (kivy.uix.button.Button): The clicked Button's
                instance.
        """
        self.infected_clr_pkr.color = self.simulation.infected_color
        self.popup_infected_color_picker.open()

    def show_recovered_color_picker(self, instance):
        """ Method that opens the popup_recovered_color_picker popup.

        Args:
            instance (kivy.uix.button.Button): The clicked Button's
                instance.
        """
        self.recovered_clr_pkr.color = self.simulation.recovered_color
        self.popup_recovered_color_picker.open()

    def save_color(self, instance, type):
        """ Method that saves the value of the color picker to its
            corresponding value in the simulation.

        Args:
            instance (kivy.uix.button.Button): The clicked Button's
                instance.
            type (String): A String that indicates the individual type.
        """
        match type:
            case 'healthy':
                self.simulation.healthy_color = self.healthy_clr_pkr.color
                self.popup_healthy_color_picker.dismiss()
            case 'infected':
                self.simulation.infected_color = self.infected_clr_pkr.color
                self.popup_infected_color_picker.dismiss()
            case 'recovered':
                self.simulation.recovered_color = self.recovered_clr_pkr.color
                self.popup_recovered_color_picker.dismiss()

    def cancel_color(self, instance, type):
        """ Method that closes the corresponding color picker popup.

        Args:
            instance (kivy.uix.button.Button): The clicked Button's
                instance.
            type (String): A String that indicates the individual type.
        """
        match type:
            case 'healthy':
                self.popup_healthy_color_picker.dismiss()
            case 'infected':
                self.popup_infected_color_picker.dismiss()
            case 'recovered':
                self.popup_recovered_color_picker.dismiss()
