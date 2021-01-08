from kivy.app import App

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder


class MainMenuWindow(Screen):
    pass


class LevelWindow(Screen):
    pass


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
