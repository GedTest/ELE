import os, threading
from kivy.app import App

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder

def thread_lvl1():
    os.system("python BuildTheCircuit.py")
def thread_lvl2():
    pass    
def thread_lvl3():
    pass

# Creates new thread in which the Python program is going to run 
Thread_lvl1 = threading.Thread(target=thread_lvl1)
Thread_lvl2 = threading.Thread(target=thread_lvl2)
Thread_lvl3 = threading.Thread(target=thread_lvl3)   

class MainMenuWindow(Screen):
    pass


class LevelWindow(Screen):
    def __init__(self, **kwargs): 
        super(LevelWindow, self).__init__(**kwargs)

    def run_lvl1(self):
        Thread_lvl1.start()

    def run_lvl2(self):
        Thread_lvl2.start()

    def run_lvl3(self):
        Thread_lvl3.start()       


class WindowManager(ScreenManager):
    pass


# loads different .kv files
# file.kv is like a CSS to HTML, basically styles
kv = Builder.load_file('Gui.kv')


class MainMenu(App):
    def build(self):
        return kv


if __name__ == '__main__':
    MainMenu().run()
