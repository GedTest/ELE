import pygame
from Components import Resistor, Diode, Button

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


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
        component.Draw(screen)

    t_btn.Draw(mouse, screen)
    f_btn.Draw(mouse, screen)

    pygame.display.flip()
    pygame.display.update()
pygame.quit()
