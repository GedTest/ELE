import pygame
from pygame.constants import MOUSEBUTTONDOWN
from Components import Button
from task_loader import load_scheme
from constants import *

pygame.init()

next_btn = Button(520, 400, 150, 100, (170, 170, 170), "Další")
end_btn = Button(520, 400, 150, 100, (170, 170, 170), "Konec")

win_font = pygame.font.SysFont('Consolas', 60)
win_screen = win_font.render("Výborně!", True, (0, 0, 0))

end_font = pygame.font.SysFont('Consolas', 60)
end_screen = win_font.render("Konec", True, (0, 0, 0))


def next_round(screen, mouse, task_id, components, tasks):
    # Diplay a text and button on the screen
    screen.blit(win_screen, ((SCREEN_WIDTH - win_screen.get_width()) /
                             2, ((SCREEN_HEIGHT - win_screen.get_height())/2)-50))

    next_btn.draw(mouse, screen)

    for e in pygame.event.get():
        # checks if a mouse is clicked
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                if next_btn.is_clickable(mouse):
                    load_scheme(tasks[task_id], components)
                    return True


def end_round(screen, mouse):
    screen.blit(end_screen, ((SCREEN_WIDTH - win_screen.get_width()) /
                             2, ((SCREEN_HEIGHT - win_screen.get_height())/2)-50))

    end_btn.draw(mouse, screen)

    for e in pygame.event.get():
        # checks if a mouse is clicked
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                if end_btn.is_clickable(mouse):
                    return True
