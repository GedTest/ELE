from kivy.app import App

from kivy.uix.widget import Widget
from kivy.lang import Builder

# loads different .kv files
Builder.load_file('box.kv')


class Box(Widget):

    def press(self):  # change scene
        pass

class MainMenu(App):
    def build(self):
        return Box()

if __name__ == '__main__':
    MainMenu().run()
