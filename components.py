import pygame
from math import sqrt
from constants import *

"""
This file contents list of component classes used in our game.
Classes are:
    Button
    Diode
    Resistor
    Switch
    PowerSupply
    MultiMeter
"""


class Button(pygame.Rect):
    """Simple Button class that checks if is button clicked via
    collision function. Also, renders self on the screen."""

    def __init__(self, left, top, width, height, color, text):
        super(Button, self).__init__(self)
        self.text = text
        self.font = pygame.font.SysFont('Consolas', 40)

        self.left = left
        self.top = top
        self.width = width
        self.height = height

        self.light_color = color
        sub = (70, 70, 70)

        # darker color for button pressed state
        self.dark_color = tuple(color[i] - sub[i] for i in range(len(color)))
        self.state_color = self.light_color

    def is_clickable(self, mouse):
        """Check if the mouse is within rect borders of a given object"""
        return self.left <= mouse[0] <= self.left + self.width and \
            self.top <= mouse[1] <= self.top + self.height

    def draw(self, mouse, screen):
        self.state_color = self.light_color if self.is_clickable(
            mouse) else self.dark_color
        pygame.draw.rect(screen, self.state_color, [
                         self.left, self.top, self.width, self.height])
        screen.blit(self.font.render(self.text, True, COLOR_GREEN),
                    (self.left + 20, self.top + 30))


class Component:
    """Base class for all components"""

    def __init__(self, value, left, top, is_invisible=False, is_choosable=False):
        self.font = pygame.font.SysFont('Consolas', 40)
        self.value = value
        self.left = left
        self.top = top
        self.is_invisible = is_invisible
        self.is_choosable = is_choosable

        if self.is_invisible:
            self.color = COLOR_WHITE
            self.name = ""

        else:
            self.color = COLOR_BLACK

    def is_colliding(self, component):
        """Handles collision with these objects: Diode, Resistor, PowerSupply"""
        if type(component) is Diode:
            distance = sqrt(((self.left - component.left) ** 2)
                            + ((self.top - component.top) ** 2))
            return distance <= component.radius

        if type(component) is Resistor:
            return component.left <= self.left <= component.left + component.width and \
                   component.top <= self.top <= component.top + component.height

        if type(component) is PowerSupply:
            return component.left <= self.left <= component.left + 35 \
                   and component.top - 50 <= self.top <= component.top + 50

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Diode(Component):
    """Simple Diode class that renders self on the screen, checks
    collision with the mouse and can switch between light modes."""

    def __init__(self, name, value, left, top, radius, is_invisible=False, is_choosable=False):
        super().__init__(value, left, top, is_invisible, is_choosable)
        self.name = name if not self.is_choosable else "D?"
        self.unit = "W"
        self.radius = radius
        self.__switch_on = COLOR_YELLOW
        self.__switch_off = COLOR_WHITE
        self.light = self.switch_off

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                           (self.left, self.top), self.radius)
        pygame.draw.circle(screen, self.light,
                           (self.left, self.top), self.radius - 5)
        pygame.draw.line(screen, self.color, (self.left - self.radius / 1.5, self.top - self.radius / 1.5),
                         (self.left + self.radius / 1.5, self.top + self.radius / 1.5), 7)
        pygame.draw.line(screen, self.color, (self.left - self.radius / 1.5, self.top + self.radius / 1.5),
                         (self.left + self.radius / 1.5, self.top - self.radius / 1.5), 7)
        screen.blit(self.font.render(self.name, True, self.color),
                    (self.left, self.top+self.radius))

    def collide_with_mouse(self, mouse):
        """Check if the mouse position is shorter or equal than the radius"""
        distance = sqrt(((self.left - mouse[0]) ** 2) + ((self.top - mouse[1]) ** 2))
        return distance <= self.radius

    def is_colliding(self, other_object):
        if type(other_object) is Diode:
            return True
        else:
            return False

    @property
    def switch_on(self):
        return self.__switch_on

    @property
    def switch_off(self):
        return self.__switch_off

    def on(self):
        """Turn the light on"""
        self.light = self.switch_on

    def off(self):
        """Turn the light off"""
        self.light = self.switch_off


class Resistor(Component):
    """Simple Resistor class that renders self on the screen."""

    def __init__(self, name, value, left, top, is_vertical=False,
                 is_invisible=False, is_choosable=False, width=160, height=70):
        super().__init__(value, left, top, is_invisible, is_choosable)
        self.name = name if not self.is_choosable else "R?"
        self.unit = '\u03A9'
        self.width = width
        self.height = height

        # flip Resistor vertical if True else horizontal
        if is_vertical:
            temp = self.width
            self.width = self.height
            self.height = temp

        if self.is_invisible:
            self.color = COLOR_WHITE
            self.name = ""
        else:
            self.color = COLOR_LIGHT_GREY

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [
                         self.left, self.top, self.width, self.height])
        screen.blit(self.font.render(self.name, True,
                                     COLOR_BLACK), (self.left, self.top))

    def collide_with_mouse(self, mouse):
        """Check if the mouse is within rect borders of a given object"""
        return self.left <= mouse[0] <= self.left + self.width and \
            self.top - self.width <= mouse[1] <= self.top + self.height


class Switch(Component):
    """Simple Switch class that renders self on the screen and handles collision with the mouse"""

    def __init__(self, name, left, top, radius, mode_on=1, is_invisible=False, is_choosable=False):
        super().__init__(0.0, left, top, is_invisible, is_choosable)
        self.name = name if not self.is_choosable else "S?"
        self.width = 65
        self.radius = radius
        self.mode = mode_on

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                           (self.left, self.top), self.radius)
        pygame.draw.circle(screen, COLOR_WHITE,
                           (self.left, self.top), self.radius-3)

        pygame.draw.circle(screen, self.color,
                           (self.left+self.width, self.top), self.radius)
        pygame.draw.circle(screen, COLOR_WHITE,
                           (self.left+self.width, self.top), self.radius-3)

        pygame.draw.line(screen, COLOR_WHITE, (self.left+self.radius-1, self.top),
                         (self.left+self.width-self.radius, self.top), 15)
        pygame.draw.line(screen, self.color, (self.left, self.top-self.radius),
                         (self.left + self.width,
                          self.top-(self.radius*self.mode)), 5)
        screen.blit(self.font.render(self.name, True, self.color),
                    (self.left, self.top+self.radius))

    def collide_with_mouse(self, mouse):
        """Check if the mouse is within rect borders of a given object"""
        return self.left-self.radius <= mouse[0] <= self.left+self.width+self.radius and \
            self.top-self.radius <= mouse[1] <= self.top+7.5+self.radius


class PowerSupply(Component):
    """Simple PowerSupply class that renders self on the screen and handles collision with the mouse"""

    def __init__(self, name, value, left, top, is_invisible=False, is_choosable=False):
        super().__init__(value, left, top, is_invisible, is_choosable)
        self.name = name if not self.is_choosable else "PS?"
        self.unit = "V"
        self.width = 35
        self.small_offset = 20  # small line of component
        self.big_offset = 50    # bigger line of component

    def draw(self, screen):
        pygame.draw.line(screen, self.color,
                         (self.left, self.top - self.big_offset),
                         (self.left, self.top + self.big_offset), 5)
        pygame.draw.line(screen, COLOR_WHITE, (self.left+3, self.top),
                         (self.left+self.width, self.top), 15)
        pygame.draw.line(screen, self.color,
                         (self.left+self.width, self.top-self.small_offset),
                         (self.left+self.width, self.top+self.small_offset), 5)
        screen.blit(self.font.render(self.name, True, self.color),
                    (self.left, self.top+self.big_offset))

    def collide_with_mouse(self, mouse):
        """Check if the mouse is within rect borders of a given object"""
        return self.left <= mouse[0] <= self.left+self.width and \
            self.top-self.big_offset <= mouse[1] <= self.top+self.big_offset


class MultiMeter(pygame.Rect):
    """Simple MultiMeter class inherited from 'pygame.Rect'
    that renders self on the screen and handles collision with
    the other objects. And show their values with units on its screen."""

    def __init__(self, left, top, width, height):
        super(MultiMeter, self).__init__(self)

        # multimeter's properties
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = (255, 90, 90)
        self.font = pygame.font.SysFont('Consolas', 28)
        self.display_font = pygame.font.SysFont('Consolas', 50)
        self.name = "Multi-o-meter"
        self.display_text = "0.0"

        # pin's properties
        self.pin_left = self.left+75
        self.pin_top = self.top+self.height+50
        self.pin_radius = 15

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [
                         self.left, self.top, self.width, self.height])
        pygame.draw.rect(screen, COLOR_WHITE, [
                         self.left+10, self.top+10, 180, 100])

        screen.blit(self.font.render(self.name, True, COLOR_BLACK),
                    (self.left, self.top+self.height/2))
        screen.blit(self.display_font.render
                    (self.display_text, True, COLOR_BLACK),
                    (self.left+15, self.top+50))
        pygame.draw.line(screen, COLOR_BLACK,
                         (self.left+75, self.top+self.height-50),
                         (self.pin_left, self.pin_top), 5)
        pygame.draw.circle(screen, COLOR_BLACK,
                           (self.pin_left, self.pin_top), self.pin_radius)

    def collide_with_mouse(self, mouse):
        """Check if the mouse position is shorter or equal than the radius"""
        distance = sqrt(
            ((self.pin_left-mouse[0])**2) + ((self.pin_top-mouse[1])**2))
        return distance <= self.pin_radius

    def is_colliding(self, other_object):
        """Handles collision with these objects: Diode, Resistor, PowerSupply"""
        if type(other_object) is Diode:
            distance = sqrt(((self.pin_left - other_object.left)
                            ** 2) + ((self.pin_top - other_object.top)**2))
            return distance <= self.pin_radius + other_object.radius

        if type(other_object) is Resistor:
            return other_object.left <= self.pin_left <= other_object.left + other_object.width and \
                other_object.top <= self.pin_top <= other_object.top + other_object.height

        if type(other_object) is PowerSupply:
            return other_object.left <= self.pin_left <= other_object.left+35 \
                   and other_object.top-50 <= self.pin_top <= other_object.top+50

    def follow_mouse(self, mouse):
        """Multimeter follows the mouse when dragged"""
        self.pin_left = mouse[0]
        self.pin_top = mouse[1]

    def reset(self):
        """If mouse isn't dragging a pin, reset its position and
        display zero values"""
        self.pin_left = 1055
        self.pin_top = 450
        self.display_text = "0.0"
