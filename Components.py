import pygame


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


class Diode():
    def __init__(self, x, y, radius):
        super(Diode,self).__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.__switch_on = (255, 255, 0)
        self.__switch_off = (255, 255, 255)
        self.light = self.switch_off

    def Draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius)
        pygame.draw.circle(screen, self.light,
                           (self.x, self.y), self.radius - 5)

        pygame.draw.line(screen, (0, 0, 0), (self.x - self.radius / 1.5, self.y - self.radius / 1.5),
                         (self.x + self.radius / 1.5, self.y + self.radius / 1.5), 7)
        pygame.draw.line(screen, (0, 0, 0), (self.x - self.radius / 1.5, self.y + self.radius / 1.5),
                         (self.x + self.radius / 1.5, self.y - self.radius / 1.5), 7)

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
    def __init__(self, left, top, width, height, color, name):
        super(Resistor,self).__init__(self)
        self.left = left
        self.top = top
        self.width = width
        self.height = height

        self.color = color
        self.name = name
        self.font = pygame.font.SysFont('Consolas', 40)

    def Draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.left, self.top, self.width, self.height])
        screen.blit(self.font.render(self.name, True,
                                     (0, 0, 0)), (self.left, self.top))

