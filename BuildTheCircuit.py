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

offset_x = 0
offset_y = 0
task_id = 0
draging = False
won_the_round = False
running = True

load_scheme(tasks[task_id], components)

while running:
    mouse = pygame.mouse.get_pos()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        # checks if a mouse is clicked
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                draging = True
                #if r3.collide_with_mouse(e.pos):
                if r3.collidepoint(e.pos):
                    print("asdsa")
                    mouse_x, mouse_y = e.pos
                    offset_x = r3.left - mouse_x
                    offset_y = r3.top - mouse_y

        elif e.type == MOUSEBUTTONUP:
            if e.button == 1:
                draging = False
                #if r3.is_colliding(r1):
                if r3.colliderect(r1):
                    won_the_round = True
                    task_id += 1
                    r3.width = 0
                    r3.height = 0
                    r3.name = ""
                    r1.color = (90,90,90)
                    r1.name = "R1"
                   
                    print("volam")
                else:
                    r3.left = 1100
                    r3.top = 50
                
        elif e.type == pygame.MOUSEMOTION:
            if draging and r3.collidepoint(e.pos):
                mouse_x, mouse_y = e.pos
                r3.left = mouse_x + offset_x
                r3.top = mouse_y + offset_y

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
            won_the_round = False

    elif task_id == len(tasks):
        if end_round(screen,mouse):
            pygame.quit()
        
    for component in components:
        if component.name == "R1": 
            r1 = component
            r1.name = ""
    
        if component.name == "R3":
            r3 = component
            r3.name = "R?" 
            
        component.draw(screen)
    
    pygame.display.flip()
    pygame.display.update()
pygame.quit()
