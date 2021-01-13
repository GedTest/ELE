import os
import threading as th
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder


def thread_build():
    os.system("python levels/build_the_circuit.py")


def thread_true_false():
    os.system("python levels/true_false_circuit.py")


# Creates new thread in which the Python program is going to run
Thread_build = th.Thread(target=thread_build)
Thread_true_false = th.Thread(target=thread_true_false)


class MainMenuWindow(Screen):
    pass


class LevelWindow(Screen):
    def __init__(self, **kwargs):
        super(LevelWindow, self).__init__(**kwargs)

    # Starts build the circuit level
    def run_build(self):
        Thread_build.start()

    # Starts true false circuit level
    def run_true_false(self):
        Thread_true_false.start()


class WindowManager(ScreenManager):
    pass


# loads different .kv files
# file.kv is like a CSS to HTML, basically styles
kv = Builder.load_file('gui.kv')


class MainMenu(App):
    def build(self):
        return kv


if __name__ == '__main__':
    MainMenu().run()
