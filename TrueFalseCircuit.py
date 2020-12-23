import pygame


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


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

    def Draw(self, mouse):
        self.state_color = self.light_color if self.is_clickable(mouse) else self.dark_color
        pygame.draw.rect(screen, self.state_color, [self.left, self.top, self.width, self.height])
        screen.blit(self.font.render(self.text, True, (0, 255, 0)), (self.left + 20, self.top + 30))


class Diode:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.__switch_on = (255, 255, 0)
        self.__switch_off = (255, 255, 255)
        self.light = self.switch_off

    def Draw(self):
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius)
        pygame.draw.circle(screen, self.light, (self.x, self.y), self.radius - 5)

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


class Resistor:
    def __init__(self, left, top, width, height, color, name):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

        self.color = color
        self.name = name
        self.font = pygame.font.SysFont('Consolas', 40)

    def Draw(self):
        pygame.draw.rect(screen, self.color, [self.left, self.top, self.width, self.height])
        screen.blit(self.font.render(self.name, True, (0, 0, 0)), (self.left, self.top))


f_btn = Button(1000, 600, 150, 100, (170, 170, 170), "False")
t_btn = Button(50, 600, 150, 100, (170, 170, 170), "True")

d1 = Diode(500, 150, 50)
r1 = Resistor(600, 125, 160, 70, (90, 90, 90), "R1")
r2 = Resistor(500, 610, 160, 70, (90, 90, 90), "R2")
r3 = Resistor(225, 455, 70, 160, (90, 90, 90), "R3")

components = (d1, r1, r2, r3)

running = True
while running:
    mouse = pygame.mouse.get_pos()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        # checks if a mouse is clicked
        if e.type == pygame.MOUSEBUTTONDOWN:
            if t_btn.is_clickable(mouse):
                print(t_btn.text)
                d1.on()

            elif f_btn.is_clickable(mouse):
                print(f_btn.text)
                d1.off()

    # Background color
    screen.fill((255, 255, 255))

    # Display a circuit rectangle
    pygame.draw.rect(screen, (0, 0, 0), [250, 150, 700, 500])
    pygame.draw.rect(screen, (255, 255, 255), [260, 160, 680, 480])

    # Display a text on the screen
    font = pygame.font.SysFont('Consolas', 30)
    heading = font.render("True or False?", True, (255, 0, 0))
    screen.blit(heading, (32, 48))

    for component in components:
        component.Draw()

    t_btn.Draw(mouse)
    f_btn.Draw(mouse)

    pygame.display.flip()
    pygame.display.update()
pygame.quit()
