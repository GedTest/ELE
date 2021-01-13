import pygame
from pygame.constants import MOUSEBUTTONDOWN
from components import Button
from task_loader import load_scheme
from constants import *

pygame.init()

font_win = pygame.font.SysFont('Consolas', 60)
font_end = pygame.font.SysFont('Consolas', 40)
win_screen = font_win.render("Výborně!", True, COLOR_BLACK)
end_screen = font_end.render("Dokončil jsi všechny úrovně!", True, COLOR_BLACK)

next_btn = Button(520, 400, 150, 100, COLOR_DARK_GREY, "Další")
end_btn = Button(450 , 450, 280, 100, COLOR_DARK_GREY, "Ukončit hru")

def next_round(screen, mouse, task_id, all_components, tasks):
    # Diplay a text and button on the screen
    screen.blit(win_screen, ((SCREEN_WIDTH - win_screen.get_width()) /
                             2, ((SCREEN_HEIGHT - win_screen.get_height())/2)-50))

    next_btn.draw(mouse, screen)

    for e in pygame.event.get():
        # checks if a mouse is clicked
        if e.type == MOUSEBUTTONDOWN:
            if e.button == MOUSE_LEFT_CLICK:
                if next_btn.is_clickable(mouse):
                    load_scheme(tasks[task_id], all_components)
                    return True


def end_round(screen, mouse):
    screen.blit(end_screen, ((SCREEN_WIDTH - end_screen.get_width()) / 2, (SCREEN_HEIGHT - end_screen.get_height())/2))

    end_btn.draw(mouse, screen)

    # if button is clicked, then the game ends
    for e in pygame.event.get():
        if e.type == MOUSEBUTTONDOWN:
            if e.button == MOUSE_LEFT_CLICK:
                if end_btn.is_clickable(mouse):
                    return True
