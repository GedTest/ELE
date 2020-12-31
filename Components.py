import pygame

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)


class Button(pygame.Rect):
    def __init__(self, left, top, width, height, color, text):
        super().__init__(self)
        self.text = text
        self.font = pygame.font.SysFont('Consolas', 40)

        self.left = left
        self.top = top
        self.width = width
        self.height = height

        self.light_color = color
        sub = (70, 70, 70)
        self.dark_color = tuple(color[i] - sub[i] for i in range(len(color)))
        self.state_color = self.light_color

    def is_clickable(self, mouse):
        return self.left <= mouse[0] <= self.left + self.width and self.top <= mouse[1] <= self.top + self.height

    def Draw(self, mouse, screen):
        self.state_color = self.light_color if self.is_clickable(
            mouse) else self.dark_color
        pygame.draw.rect(screen, self.state_color, [
                         self.left, self.top, self.width, self.height])
        screen.blit(self.font.render(self.text, True, (0, 255, 0)),
                    (self.left + 20, self.top + 30))


class Diode:
    def __init__(self, name, power, voltage, left, top, radius):
        super(Diode, self).__init__()
        self.name = name
        self.__power = power
        self.__voltage = voltage
        self.font = pygame.font.SysFont('Consolas', 40)
        self.left = left
        self.top = top
        self.radius = radius
        self.__switch_on = (255, 255, 0)
        self.__switch_off = COLOR_WHITE
        self.light = self.switch_off

    def Draw(self, screen):
        pygame.draw.circle(screen, COLOR_BLACK, (self.left, self.top), self.radius)
        pygame.draw.circle(screen, self.light,
                           (self.left, self.top), self.radius - 5)

        pygame.draw.line(screen, COLOR_BLACK, (self.left - self.radius / 1.5, self.top - self.radius / 1.5),
                         (self.left + self.radius / 1.5, self.top + self.radius / 1.5), 7)
        pygame.draw.line(screen, COLOR_BLACK, (self.left - self.radius / 1.5, self.top + self.radius / 1.5),
                         (self.left + self.radius / 1.5, self.top - self.radius / 1.5), 7)
        screen.blit(self.font.render(self.name, True, COLOR_BLACK), (self.left, self.top+self.radius))

    @property
    def switch_on(self):
        return self.__switch_on

    @property
    def switch_off(self):
        return self.__switch_off

    def on(self):
        self.light = self.switch_on

    def off(self):
        self.light = self.switch_off


class Resistor(pygame.Rect):
    def __init__(self, name, resistance, left, top, is_vertical=False, width=160, height=70):
        super(Resistor, self).__init__(self)
        self.name = name
        self.font = pygame.font.SysFont('Consolas', 40)
        self.__resistance = resistance
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        if is_vertical:
            value = self.width
            self.width = self.height
            self.height = value

        self.color = (90, 90, 90)

    def Draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.left, self.top, self.width, self.height])
        screen.blit(self.font.render(self.name, True, COLOR_BLACK), (self.left, self.top))

    @property
    def resistance(self):
        return self.__resistance


class Switch:
    def __init__(self, name, left, top, radius, mode_on=1):
        self.name = name
        self.font = pygame.font.SysFont('Consolas', 40)
        self.left = left
        self.top = top
        self.radius = radius
        self.mode = mode_on

    def Draw(self, screen):
        pygame.draw.circle(screen, COLOR_BLACK, (self.left, self.top), self.radius)
        pygame.draw.circle(screen, COLOR_WHITE, (self.left, self.top), self.radius-3)

        pygame.draw.circle(screen, COLOR_BLACK, (self.left+65, self.top), self.radius)
        pygame.draw.circle(screen, COLOR_WHITE, (self.left+65, self.top), self.radius-3)

        pygame.draw.line(screen, COLOR_WHITE, (self.left+self.radius-1, self.top),
                         (self.left+65-self.radius, self.top), 15)
        pygame.draw.line(screen, COLOR_BLACK, (self.left, self.top-self.radius),
                         (self.left + 65, self.top-(self.radius*self.mode)), 5)
        screen.blit(self.font.render(self.name, True, COLOR_BLACK), (self.left, self.top+self.radius))


class PowerSupply:
    def __init__(self, name, voltage, left, top):
        self.name = name
        self.font = pygame.font.SysFont('Consolas', 40)
        self.voltage = voltage
        self.left = left
        self.top = top
        self.small_offset = 20
        self.big_offset = 50

    def Draw(self, screen):
        pygame.draw.line(screen, COLOR_BLACK, (self.left, self.top - self.big_offset),
                         (self.left, self.top + self.big_offset), 5)
        pygame.draw.line(screen, COLOR_WHITE, (self.left+3, self.top),
                         (self.left+35, self.top), 15)
        pygame.draw.line(screen, COLOR_BLACK, (self.left+35, self.top-self.small_offset),
                         (self.left+35, self.top+self.small_offset), 5)
        screen.blit(self.font.render(self.name, True, COLOR_BLACK), (self.left, self.top+self.big_offset))
