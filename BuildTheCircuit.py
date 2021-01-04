import pygame, json
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.event import event_name
from Components import Resistor, Diode, Button, PowerSupply, Switch

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

with open("data_build_circuit.json", "r") as components_file:
    data = json.load(components_file)

components = []
for key in data.keys():
    if key != "level_answer":
        if data[key]["type"] == "Diode":
            components.append(Diode(data[key]["name"], data[key]["value"], data[key]["left"],
                                    data[key]["top"], data[key]["radius"]))
        if data[key]["type"] == "Resistor":
            components.append(Resistor(data[key]["name"], data[key]["value"], data[key]["left"],
                                    data[key]["top"], data[key]["is_vertical"], data[key]["is_invisible"]))
        if data[key]["type"] == "Switch":
            components.append(Switch(data[key]["name"], data[key]["left"], data[key]["top"], data[key]["radius"],
                                    data[key]["mode_on"]))
        if data[key]["type"] == "PowerSupply":
            components.append(PowerSupply(data[key]["name"], data[key]["value"], data[key]["left"], data[key]["top"]))
    else:
        level_answer = data[key]

offset_x = 0
offset_y = 0
draging = False
won_the_round = False
running = True

for choose_component in components:
    if choose_component.name == "R1": 
        r1 = choose_component
        r1.name = ""
    if choose_component.name == "R3":
        r3 = choose_component
        r3.name = "R?"
        

while running:
    mouse = pygame.mouse.get_pos()
        
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        # checks if a mouse is clicked
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                draging = True
                if r3.collidepoint(e.pos):
                    mouse_x, mouse_y = e.pos
                    offset_x = r3.x - mouse_x
                    offset_y = r3.y - mouse_y

        elif e.type == MOUSEBUTTONUP:
            if e.button == 1:
                draging = False
                if r3.colliderect(r1):
                    r3.width = 0
                    r3.height = 0
                    r3.name = ""
                    r1.color = (90,90,90)
                    r1.name = "R1"
                    won_the_round = True
                    
                else:
                    r3.x = 1100
                    r3.y = 50

        elif e.type == pygame.MOUSEMOTION:
            if draging and r3.collidepoint(e.pos):
                mouse_x, mouse_y = e.pos
                r3.x = mouse_x + offset_x
                r3.y = mouse_y + offset_y

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
        component.draw(screen)

    pygame.display.flip()
    pygame.display.update()
pygame.quit()
