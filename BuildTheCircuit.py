import pygame
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.event import event_name
from Components import Resistor, Diode, Button

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


d1 = Diode(500, 150, 50)
r1 = Resistor(600, 125, 160, 70, (255, 255, 255), "")
r2 = Resistor(500, 610, 160, 70, (0, 0, 0), "R2")
r3 = Resistor(225, 455, 70, 160, (0, 0, 0), "R3")
r4 = Resistor(1100, 50, 70, 160, (0, 0, 0), "")

components = (d1, r1, r2, r3, r4)
components_to_choose = (r4)

offset_x = 0
offset_y = 0
draging = False
won_the_round = False
running = True
while running:
    mouse = pygame.mouse.get_pos()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        # checks if a mouse is clicked
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                draging = True
                if r4.collidepoint(e.pos):
                    mouse_x, mouse_y = e.pos
                    offset_x = r4.x - mouse_x
                    offset_y = r4.y - mouse_y

        elif e.type == MOUSEBUTTONUP:
            if e.button == 1:
                draging = False
                if r4.colliderect(r1):
                    r4.width = 0
                    r4.height = 0
                    r1.color = (0, 0, 0)
                    won_the_round = True
                    
                else:
                    r4.x = 1100
                    r4.y = 50

        elif e.type == pygame.MOUSEMOTION:
            if draging and r4.collidepoint(e.pos):
                mouse_x, mouse_y = e.pos
                r4.x = mouse_x + offset_x
                r4.y = mouse_y + offset_y

    # Background color
    screen.fill((255, 255, 255))

    # Display a circuit rectangle
    pygame.draw.rect(screen, (0, 0, 0), [250, 150, 700, 500])
    pygame.draw.rect(screen, (255, 255, 255), [260, 160, 680, 480])

    # Display a text on the screen
    font = pygame.font.SysFont('Consolas', 30)
    win_font = pygame.font.SysFont('Consolas', 60)
    heading = font.render("Zapoj obvod", True, (0, 0, 0))
    win_screen = win_font.render("Výborně!", True, (0, 0, 0))
    screen.blit(heading, (32, 48))
    if won_the_round:
        screen.blit(win_screen, ((SCREEN_WIDTH - win_screen.get_width())/2 , (SCREEN_HEIGHT - win_screen.get_height())/2))

    for component in components:
        component.Draw(screen)

    pygame.display.flip()
    pygame.display.update()
pygame.quit()
