'''
Canvas stress
=============

This example tests the performance of our Graphics engine by drawing large
numbers of small squares. You should see a black canvas with buttons and a
label at the bottom. Pressing the buttons adds small colored squares to the
canvas.

'''
from threading import Thread
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from random import random
from functools import partial
from kivy.animation import Animation
from kivy.uix.slider import Slider


class CircularButton(ButtonBehavior, Label):

    @property
    def direction(self):
        return self.direction

    @direction.setter
    def direction(self, angle):
        self.direction = angle


class Menu(BoxLayout):

    def __init__(self, main, layout, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.threads_slider_label = Label(text='Threads:')
        self.threads_slider_value_label = Label(text='0')
        self.threads_slider = Slider(min=0, max=100, value=0)
        self.add_widget(self.threads_slider)
        self.add_widget(self.threads_slider_label)
        self.add_widget(self.threads_slider_value_label)
        self.threads_slider.bind(value=self.on_value)
        self.btn_add_thread = Button(text='+ 1 Thread',
                                     on_press=partial(
                                         main.add_thread,
                                         self.threads_slider,
                                         layout, 1))
        self.btn_reset = Button(text='Reset',
                                on_press=partial(
                                    main.reset_threads,
                                    self.threads_slider, layout))
        self.btn_play = Button(text='Start/Pause',
                               on_press=partial(
                                    main.reset_threads,
                                    self.threads_slider, layout))
        self.add_widget(self.btn_add_thread)
        self.add_widget(self.btn_play)
        self.add_widget(self.btn_reset)

    def on_value(self, instance, threads):
        self.threads_slider_value_label.text = "% d" % threads


class MainWindow(App):

    @property
    def threads(self):
        return self._threads

    @threads.setter
    def threads(self, threads: list):
        self._threads = threads

    def animate(self, instance):
        # create an animation object. This object could be stored
        # and reused each call or reused across different widgets.
        # += is a sequential step, while &= is in parallel
        animation = Animation(pos=(100, 100), t='out_bounce')
        animation += Animation(pos=(200, 100), t='out_bounce')
        animation &= Animation(size=(500, 500))
        animation += Animation(size=(100, 50))

        # apply the animation on the button, passed in the "instance" argument
        # Notice that default 'click' animation (changing the button
        # color while the mouse is down) is unchanged.
        animation.start(instance)

    def reset_threads(self, slider, wid, *largs):
        slider.value = 0
        wid.canvas.clear()

    def add_thread(self, slider, wid, count, *largs):
        slider.value += count
        with wid.canvas:
            for x in range(count):
                # Color(r(), 1, 1, mode='hsv')
                CircularButton(size=(20, 20),
                               pos=((random() * wid.width + wid.x,
                                    random() * wid.height + wid.y)), text="")

    def build(self):
        self.threads = []
        root = BoxLayout(orientation='vertical')
        layout = BoxLayout(size_hint=(1, None), height=700)
        menu = Menu(self, layout)
        root.add_widget(layout)
        root.add_widget(menu)
        return root


if __name__ == '__main__':
    MainWindow().run()
