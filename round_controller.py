import pygame
from pygame.constants import K_NUMLOCKCLEAR, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from components import Button
from task_loader import load_scheme
from constants import *

pygame.init()

next_btn = Button(520, 400, 150, 100, COLOR_GREY, "Další")
end_btn = Button(520, 400, 150, 100, COLOR_GREY, "Konec")

win_font = pygame.font.SysFont('Consolas', 60)
win_screen = win_font.render("Výborně!", True, COLOR_GREEN)

end_font = pygame.font.SysFont('Consolas', 60)
end_screen = win_font.render("Konec", True, COLOR_BLACK)


def next_round(screen, mouse, task_id, components, tasks):
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
