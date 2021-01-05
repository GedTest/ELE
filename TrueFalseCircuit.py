import pygame

import json
from Components import Resistor, Diode, Button, Switch, PowerSupply, MultiMeter, COLOR_BLACK, COLOR_WHITE

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

level_answer = ''
player_guess = ''

f_btn = Button(1000, 600, 150, 100, (170, 170, 170), "No")
t_btn = Button(50, 600, 150, 100, (170, 170, 170), "Yes")

ps5 = PowerSupply("PS5", 230.0, 450, 400)

with open("data_file.json", "r") as components_file:
    data = json.load(components_file)

components = [ps5]
for key in data.keys():
    if key != "level_answer":
        if data[key]["type"] == "Diode":
            components.append(Diode(data[key]["name"], data[key]["value"], data[key]["left"],
                                    data[key]["top"], data[key]["radius"]))
        if data[key]["type"] == "Resistor":
            components.append(Resistor(data[key]["name"], data[key]["value"], data[key]["left"],
                                       data[key]["top"], data[key]["is_vertical"]))
        if data[key]["type"] == "Switch":
            components.append(Switch(data[key]["name"], data[key]["left"], data[key]["top"], data[key]["radius"],
                                     data[key]["mode_on"]))
        if data[key]["type"] == "PowerSupply":
            components.append(PowerSupply(data[key]["name"], data[key]["value"], data[key]["left"], data[key]["top"]))
    else:
        level_answer = data[key]

multi_meter = MultiMeter(980, 100, 200, 300)
components.append(multi_meter)

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

            elif ps5.collide_with_mouse(mouse):
                print("Hello")

        # ----------multi-meter----------
            if e.button == 1 and multi_meter.collide_with_mouse(e.pos):
                dragging = True

        elif e.type == pygame.MOUSEMOTION:
            if dragging:
                multi_meter.follow_mouse(e.pos)

        elif e.type == pygame.MOUSEBUTTONUP:
            dragging = False
            multi_meter.pin_left = 1055
            multi_meter.pin_top = 450
        # ----------multi-meter----------

    # Background color
    screen.fill(COLOR_WHITE)

    # Display a circuit rectangle
    pygame.draw.rect(screen, COLOR_BLACK, [250, 150, 700, 500])
    pygame.draw.rect(screen, COLOR_WHITE, [260, 160, 680, 480])

    for component in components:
        component.draw(screen)
        if multi_meter.is_colliding(component):
            multi_meter.display_text = str(component.value) + component.unit

    t_btn.draw(mouse, screen)
    f_btn.draw(mouse, screen)

    # Display a text on the screen
    font = pygame.font.SysFont('Consolas', 30)
    heading = font.render("Is this scheme working??", True, (255, 0, 0))
    screen.blit(heading, (32, 48))

    # Compare player's guest with correct answer and display it on the screen
    if player_guess:
        result = "Correct" if player_guess == level_answer else "Incorrect"
        font = pygame.font.SysFont('Consolas', 60)
        text = font.render(result, True, (0, 255, 0))
        screen.blit(text, (SCREEN_WIDTH/2-125, SCREEN_HEIGHT/2))

    pygame.display.flip()
    pygame.display.update()
pygame.quit()
