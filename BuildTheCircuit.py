import pygame
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from Components import Button
from data_build_circuit import task1, task2, task3
from task_loader import load_scheme
from constants import *
from round_controller import end_round, next_round

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

next_btn = Button(520, 400, 150, 100, (170, 170, 170), "Další")

tasks = [task1, task2, task3]
components = []
invisible_components = []
choosable_components = []

offset_x = 0
offset_y = 0
task_id = 0
ch_left = 0
ch_top = 0
draging = False
won_the_round = False
running = True


def load_list():
    for component in components:
        if component.is_invisible: 
            invisible_components.append(component)
        if component.is_choosable:
            choosable_components.append(component)

load_scheme(tasks[task_id], components)
load_list()

while running:
    mouse = pygame.mouse.get_pos()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
       
        # checks if a mouse is clicked
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                draging = True
                for ch_component in choosable_components:
                    if ch_component.collide_with_mouse(e.pos):
                        mouse_x, mouse_y = e.pos
                        ch_top = ch_component.top
                        ch_left = ch_component.left
                        print(ch_top)
                        print(ch_left)
                        offset_x = ch_component.left - mouse_x
                        offset_y = ch_component.top - mouse_y

        elif e.type == MOUSEBUTTONUP:
            if e.button == 1:
                draging = False
                for ch_component in choosable_components:
                    for inv_component in invisible_components:
                        if ch_component.is_colliding(inv_component):
                            print("koliduji")
                            # Remove current choosable component from a components and choosable_components list, that it cannnot be drawn
                            choosable_components.remove(ch_component)
                            components.remove(ch_component)
                            # Invisible component will be visible 
                            inv_component.color = COLOR_BLACK

                            # if 
                            if len(choosable_components) == 0:
                                won_the_round = True
                                task_id += 1
                        else:
                            ch_component.left = 1100
                            ch_component.top = 50

        elif e.type == pygame.MOUSEMOTION:
            for ch_component in choosable_components:
                if draging and ch_component.collide_with_mouse(e.pos):
                    mouse_x, mouse_y = e.pos
                    ch_component.left = mouse_x + offset_x
                    ch_component.top = mouse_y + offset_y
           

    # Background color
    screen.fill((255, 255, 255))

    # Display a circuit rectangle
    pygame.draw.rect(screen, (0, 0, 0), [250, 150, 700, 500])
    pygame.draw.rect(screen, (255, 255, 255), [260, 160, 680, 480])

    # Display a text on the screen
    font = pygame.font.SysFont('Consolas', 30)
    heading = font.render("Zapoj obvod", True, (0, 0, 0))
    screen.blit(heading, (32, 48))

    if won_the_round and task_id != len(tasks):
        if next_round(screen, mouse, task_id, components, tasks):
            load_list()
            won_the_round = False

    if task_id == len(tasks):
        if end_round(screen,mouse):
            pygame.quit()
        
    for component in components:
        component.draw(screen)
        
    pygame.display.flip()
    pygame.display.update()
pygame.quit()
