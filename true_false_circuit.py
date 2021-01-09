import pygame
#import json
from constants import *
#from components import Resistor, Diode, Button, Switch, PowerSupply, MultiMeter
from components import Button, MultiMeter
from data_build_circuit_true_false import task1, task2, task3
from task_loader import load_scheme
from round_controller import end_round, next_round

#pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

level_answer = ''
player_guess = ''

next_btn = Button(520, 400, 150, 100, (170, 170, 170), "Další")
f_btn = Button(1000, 600, 150, 100, COLOR_DARK_GREY, "No")
t_btn = Button(50, 600, 150, 100, COLOR_DARK_GREY, "Yes")

#with open("data_file.json", "r") as components_file:
#    data = json.load(components_file)

tasks = [task1, task2, task3]
task_id = 0
won_the_round = False
all_components = []
#for key in data.keys():
#    if key != "level_answer":
#        if data[key]["type"] == "Diode":
#            all_components.append(Diode(data[key]["name"], data[key]["value"], data[key]["left"],
#                                        data[key]["top"], data[key]["radius"]))
#        if data[key]["type"] == "Resistor":
#            all_components.append(Resistor(data[key]["name"], data[key]["value"], data[key]["left"],
#                                           data[key]["top"], data[key]["is_vertical"]))
#        if data[key]["type"] == "Switch":
#            all_components.append(Switch(data[key]["name"], data[key]["left"], data[key]["top"], data[key]["radius"],
#                                         data[key]["mode_on"]))
#        if data[key]["type"] == "PowerSupply":
#            all_components.append(PowerSupply(data[key]["name"], data[key]["value"], data[key]["left"],
#                                              data[key]["top"]))
#    else:
#        level_answer = data[key]

level_answer = load_scheme(tasks[task_id], all_components)

multi_meter = MultiMeter(980, 100, 200, 300)
all_components.append(multi_meter)

dragging = False
running = True
while running:
    mouse = pygame.mouse.get_pos()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        # checks if a mouse is clicked
        if e.type == pygame.MOUSEBUTTONDOWN:
            if t_btn.is_clickable(mouse):
                player_guess = t_btn.text

            elif f_btn.is_clickable(mouse):
                player_guess = f_btn.text

        # ----------multi-meter----------
            if e.button == 1 and multi_meter.collide_with_mouse(e.pos):
                dragging = True

        elif e.type == pygame.MOUSEMOTION:
            if dragging:
                multi_meter.follow_mouse(e.pos)

        elif e.type == pygame.MOUSEBUTTONUP:
            dragging = False
            multi_meter.reset()
        # ----------multi-meter----------

    # Background color
    screen.fill(COLOR_WHITE)

    # Display a circuit rectangle
    pygame.draw.rect(screen, COLOR_BLACK, [250, 150, 700, 500])
    pygame.draw.rect(screen, COLOR_WHITE, [260, 160, 680, 480])

    for component in all_components:
        component.draw(screen)
        if multi_meter.is_colliding(component):
            multi_meter.display_text = str(component.value) + component.unit

    t_btn.draw(mouse, screen)
    f_btn.draw(mouse, screen)

    # Display a text on the screen
    font = pygame.font.SysFont('Consolas', 30)
    heading = font.render("Is this scheme working??", True, COLOR_BLACK)
    screen.blit(heading, (32, 48))

    # Compare player's guest with correct answer and display it on the screen
    if player_guess:
        #result = "Correct" if player_guess == level_answer else "Incorrect"
        #result_color = COLOR_GREEN if player_guess == level_answer else COLOR_RED
        #font = pygame.font.SysFont('Consolas', 60)
        #text = font.render(result, True, result_color)
        #screen.blit(text, (SCREEN_WIDTH/2-125, SCREEN_HEIGHT/2))

        # if player won
        if player_guess == level_answer:
            won_the_round = True
            print(task_id)
            task_id += 1
        else:
            font = pygame.font.SysFont('Consolas', 60)
            text = font.render("Špatně!", True, COLOR_RED)
            screen.blit(text, (SCREEN_WIDTH/2-125, SCREEN_HEIGHT/2))

    if won_the_round and task_id != len(tasks):
        if next_round(screen, mouse, task_id, all_components, tasks):
            won_the_round = False

    elif task_id == len(tasks):
        if end_round(screen, mouse):
            pygame.quit()

    pygame.display.flip()
    pygame.display.update()
pygame.quit()
