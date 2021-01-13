from os import terminal_size
import pygame
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from components import Button, Resistor
from task_loader import load_scheme
from constants import *
from round_controller import end_round, next_round

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

next_btn = Button(520, 400, 150, 100, COLOR_DARK_GREY, "Další")

tasks = ["task_build1", "task_build2", "task_build3"]  # list of levels
all_components = []
invisible_components = []
choosable_components = []

offset_x = 0
offset_y = 0
task_id = 0  # pointer at current 'level'
ch_top = 0
ch_left = 0
draging = False
won_the_round = False
running = True


def load_list():
    for component in all_components:
        if component.is_invisible:
            invisible_components.append(component)
        if component.is_choosable:
            choosable_components.append(component)


# Loads first scheme on screen
load_scheme(tasks[task_id], all_components)
load_list()

while running:
    # Get mouse [left, top] coordinates
    mouse = pygame.mouse.get_pos()

    for e in pygame.event.get():
        # Stands for closing app window
        if e.type == pygame.QUIT:
            running = False

        # checks if a mouse is clicked
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == MOUSE_LEFT_CLICK:
                draging = True

                # Scan through the list with choosable components
                # and controls if component collides with a mouse
                for ch_component in choosable_components:
                    if ch_component.collide_with_mouse(e.pos):
                        mouse_x, mouse_y = e.pos
                        offset_x = ch_component.left - mouse_x
                        offset_y = ch_component.top - mouse_y
                        # Save origin position values
                        ch_top = ch_component.top
                        ch_left = ch_component.left
                        ch_component.drag = True  # flag

        elif e.type == MOUSEBUTTONUP:
            if e.button == MOUSE_LEFT_CLICK:
                draging = False

                for ch_component in choosable_components:
                    if ch_component.drag:
                        # Checks collision, if it's dragged
                        for inv_component in invisible_components:
                            if ch_component.is_colliding(inv_component):
                                # Remove current choosable component from a components
                                # and choosable_components list, that it cannnot be drawn
                                choosable_components.remove(ch_component)
                                invisible_components.remove(inv_component)
                                all_components.remove(ch_component)

                                # Invisible component will be visible
                                if isinstance(inv_component, Resistor): # Exception for a resistor class
                                    inv_component.color = COLOR_LIGHT_GREY
                                    inv_component.color_text = COLOR_BLACK

                                else:
                                    inv_component.color = COLOR_BLACK

                                # Run out of components
                               # if len(choosable_components) == 0:
                                if len(choosable_components) == 0:
                                    won_the_round = True
                                    task_id += 1

                        # Reset to origin position
                        else:
                            ch_component.drag = False
                            ch_component.left = ch_left
                            ch_component.top = ch_top

        # Dragging component
        elif e.type == pygame.MOUSEMOTION:
            for ch_component in choosable_components:
                if ch_component.drag and draging:
                    mouse_x, mouse_y = e.pos
                    ch_component.left = mouse_x + offset_x
                    ch_component.top = mouse_y + offset_y

    # Background color
    screen.fill(COLOR_WHITE)

    # Display a circuit rectangle
    pygame.draw.rect(screen, COLOR_BLACK, [250, 150, 700, 500])
    pygame.draw.rect(screen, COLOR_WHITE, [260, 160, 680, 480])

    # Display a text on the screen
    font = pygame.font.SysFont('Consolas', 30)
    heading = font.render("Zapoj součastky do obvodu", True, COLOR_BLACK)
    screen.blit(heading, (32, 48))

    # When the current task is done, load next round
    if won_the_round and task_id != len(tasks):
        if next_round(screen, mouse, task_id, all_components, tasks):
            load_list()
            won_the_round = False

    # When the current task is the last one, then exit the game 
    if task_id == len(tasks):
        if end_round(screen, mouse):
            running = False

    # Display all the components 
    for component in all_components:
        component.draw(screen)

    pygame.display.flip()
    pygame.display.update()
pygame.quit()
