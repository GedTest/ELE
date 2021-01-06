import pygame
from math import sqrt

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

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)


class Button(pygame.Rect):
    """Simple Button class that checks if is button clicked via collision function. Also, renders self on the screen."""

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
        return self.left <= mouse[0] <= self.left + self.width and self.top <= mouse[1] <= self.top + self.height

    def draw(self, mouse, screen):
        self.state_color = self.light_color if self.is_clickable(
            mouse) else self.dark_color
        pygame.draw.rect(screen, self.state_color, [
                         self.left, self.top, self.width, self.height])
        screen.blit(self.font.render(self.text, True, (0, 255, 0)),
                    (self.left + 20, self.top + 30))


class Diode:
    """Simple Diode class that renders self on the screen, checks collision with the mouse
     and can switch between light modes."""

    def __init__(self, name, value, left, top, radius):
        self.name = name
        self.__value = value
        self.unit = "W"
        self.font = pygame.font.SysFont('Consolas', 40)
        self.left = left
        self.top = top
        self.radius = radius
        self.__switch_on = (255, 255, 0)
        self.__switch_off = COLOR_WHITE
        self.light = self.switch_off

    def draw(self, screen):
        pygame.draw.circle(screen, COLOR_BLACK, (self.left, self.top), self.radius)
        pygame.draw.circle(screen, self.light,
                           (self.left, self.top), self.radius - 5)

        pygame.draw.line(screen, COLOR_BLACK, (self.left - self.radius / 1.5, self.top - self.radius / 1.5),
                         (self.left + self.radius / 1.5, self.top + self.radius / 1.5), 7)
        pygame.draw.line(screen, COLOR_BLACK, (self.left - self.radius / 1.5, self.top + self.radius / 1.5),
                         (self.left + self.radius / 1.5, self.top - self.radius / 1.5), 7)
        screen.blit(self.font.render(self.name, True, COLOR_BLACK), (self.left, self.top+self.radius))

    def collide_with_mouse(self, mouse):
        """Check if the mouse position is shorter or equal than the radius"""
        hypotenuse = sqrt(((self.left - mouse[0]) ** 2) + ((self.top - mouse[1]) ** 2))
        return hypotenuse <= self.radius

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

    @property
    def value(self):
        return self.__value


class Resistor(pygame.Rect):
    """Simple Resistor class that renders self on the screen.
    Inherited from 'pygame.Rect' class"""

    def __init__(self, name, value, left, top, is_vertical=False, is_invisible=False, width=160, height=70):
        super(Resistor, self).__init__(self)
        self.name = name
        self.font = pygame.font.SysFont('Consolas', 40)
        self.__value = value
        self.unit = '\u03A9'
        self.left = left
        self.top = top
        self.width = width
        self.height = height

        # flip Resistor vertical if True else horizontal
        if is_vertical:
            temp = self.width
            self.width = self.height
            self.height = temp
            
        if is_invisible:
            self.color = (255,255,255)
        else:
            self.color = (90, 90, 90)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.left, self.top, self.width, self.height])
        screen.blit(self.font.render(self.name, True, COLOR_BLACK), (self.left, self.top))

    def collide_with_mouse(self, mouse):
        self.collidepoint(mouse)
    @property
    def value(self):
        return self.__value


class Switch:
    """Simple Switch class that renders self on the screen and handles collision with the mouse"""

    def __init__(self, name, left, top, radius, mode_on=1):
        self.name = name
        self.font = pygame.font.SysFont('Consolas', 40)
        self.left = left
        self.top = top
        self.width = 65
        self.radius = radius
        self.mode = mode_on

    def draw(self, screen):
        pygame.draw.circle(screen, COLOR_BLACK, (self.left, self.top), self.radius)
        pygame.draw.circle(screen, COLOR_WHITE, (self.left, self.top), self.radius-3)

        pygame.draw.circle(screen, COLOR_BLACK, (self.left+self.width, self.top), self.radius)
        pygame.draw.circle(screen, COLOR_WHITE, (self.left+self.width, self.top), self.radius-3)

        pygame.draw.line(screen, COLOR_WHITE, (self.left+self.radius-1, self.top),
                         (self.left+self.width-self.radius, self.top), 15)
        pygame.draw.line(screen, COLOR_BLACK, (self.left, self.top-self.radius),
                         (self.left + self.width, self.top-(self.radius*self.mode)), 5)
        screen.blit(self.font.render(self.name, True, COLOR_BLACK), (self.left, self.top+self.radius))

    def collide_with_mouse(self, mouse):
        """Check if the mouse is within rect borders of a given object"""
        return self.left-self.radius <= mouse[0] <= self.left+self.width+self.radius and \
               self.top-self.radius <= mouse[1] <= self.top+7.5+self.radius
                 
    def is_colliding(self, other_object):
        """Handles collision with these objects: Diode, Resistor, PowerSupply"""
        if type(other_object) is Diode:
            hypotenuse = sqrt(((self.left - other_object.left)**2) + ((self.top - other_object.top)**2))
            return hypotenuse <= other_object.radius

        if type(other_object) is Resistor:
            return other_object.left <= self.left <= other_object.left + other_object.width and \
                    other_object.top <= self.top <= other_object.top + other_object.height

        if type(other_object) is PowerSupply:
            return other_object.left <= self.left <= other_object.left+35 and \
                    other_object.top-50 <= self.top <= other_object.top+50   


class PowerSupply:
    """Simple PowerSupply class that renders self on the screen and handles collision with the mouse"""

    def __init__(self, name, value, left, top):
        self.name = name
        self.font = pygame.font.SysFont('Consolas', 40)
        self.value = value
        self.unit = "V"
        self.left = left
        self.top = top
        self.width = 35
        self.small_offset = 20  # small line of component
        self.big_offset = 50    # bigger line of component

    def draw(self, screen):
        pygame.draw.line(screen, COLOR_BLACK, (self.left, self.top - self.big_offset),
                         (self.left, self.top + self.big_offset), 5)
        pygame.draw.line(screen, COLOR_WHITE, (self.left+3, self.top),
                         (self.left+self.width, self.top), 15)
        pygame.draw.line(screen, COLOR_BLACK, (self.left+self.width, self.top-self.small_offset),
                         (self.left+self.width, self.top+self.small_offset), 5)
        screen.blit(self.font.render(self.name, True, COLOR_BLACK), (self.left, self.top+self.big_offset))

    def collide_with_mouse(self, mouse):
        """Check if the mouse is within rect borders of a given object"""
        return self.left <= mouse[0] <= self.left+self.width and \
               self.top-self.big_offset <= mouse[1] <= self.top+self.big_offset
  
   

class MultiMeter(pygame.Rect):
    """Simple MultiMeter class inherited from 'pygame.Rect'
    that renders self on the screen and handles collision with the other objects.
    And show their values with units on its screen."""

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
        pygame.draw.rect(screen, self.color, [self.left, self.top, self.width, self.height])
        pygame.draw.rect(screen, COLOR_WHITE, [self.left+10, self.top+10, 180, 100])

        screen.blit(self.font.render(self.name, True, COLOR_BLACK), (self.left, self.top+self.height/2))
        screen.blit(self.display_font.render(self.display_text, True, COLOR_BLACK), (self.left+15, self.top+50))
        pygame.draw.line(screen, COLOR_BLACK, (self.left+75, self.top + self.height-50),
                         (self.pin_left, self.pin_top), 5)
        pygame.draw.circle(screen, COLOR_BLACK, (self.pin_left, self.pin_top), self.pin_radius)

    def collide_with_mouse(self, mouse):
        """Check if the mouse position is shorter or equal than the radius"""
        hypotenuse = sqrt(((self.pin_left-mouse[0])**2) + ((self.pin_top-mouse[1])**2))
        return hypotenuse <= self.pin_radius

    def is_colliding(self, other_object):
        """Handles collision with these objects: Diode, Resistor, PowerSupply"""
        if type(other_object) is Diode:
            hypotenuse = sqrt(((self.pin_left - other_object.left)**2) + ((self.pin_top - other_object.top)**2))
            return hypotenuse <= self.pin_radius + other_object.radius

        if type(other_object) is Resistor:
            return other_object.left <= self.pin_left <= other_object.left + other_object.width and \
                    other_object.top <= self.pin_top <= other_object.top + other_object.height

        if type(other_object) is PowerSupply:
            return other_object.left <= self.pin_left <= other_object.left+35 and \
                   other_object.top-50 <= self.pin_top <= other_object.top+50

    def follow_mouse(self, mouse):
        """Multimeter follows the mouse when dragged"""
        self.pin_left = mouse[0]
        self.pin_top = mouse[1]