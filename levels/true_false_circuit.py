from common.constants import *
from common.components import Button, MultiMeter
from level_control.task_loader import *
from level_control.round_controller import end_round, next_round

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

next_btn = Button(520, 400, 150, 100, COLOR_DARK_GREY, "Další")
f_btn = Button(1000, 600, 150, 100, COLOR_DARK_GREY, "Ne")
t_btn = Button(50, 600, 150, 100, COLOR_DARK_GREY, "Ano")

tasks = ["task_true_false1", "task_true_false2", "task_true_false3"]  # list of levels
task_id = 0                    # pointer at current 'level'
won_the_round = False
all_components = []

level_answer = get_level_answer(tasks[task_id])
player_guess = ''

load_scheme(tasks[task_id], all_components)

multi_meter = MultiMeter(980, 100, 200, 300)
all_components.append(multi_meter)

dragging = False
running = True
while running:
    # Get mouse [left, top] coordinates
    mouse = pygame.mouse.get_pos()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        # checks if buttons are clicked
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

    # Display all of the components on the screen
    for component in all_components:
        component.draw(screen)
        if multi_meter.is_colliding(component):
            multi_meter.display_text = str(component.value) + component.unit

    # Display button on the screen
    t_btn.draw(mouse, screen)
    f_btn.draw(mouse, screen)

    # Display a text on the screen
    font = pygame.font.SysFont('Consolas', 30)
    heading = font.render("Je tohle schéma správně zapojeno??", True, COLOR_BLACK)
    screen.blit(heading, (32, 48))

    # Compare player's guest with correct answer and display it on the screen
    if player_guess:
        # If player's guess matches correct answer
        if player_guess == level_answer:
            won_the_round = True
            task_id += 1               # Increment task_id to get new scheme from array
            player_guess = ''          # Reset player's guess to none
            if task_id != len(tasks):  # Get new level answer
                level_answer = get_level_answer(tasks[task_id])

        # Else if player's guess do not matches correct answer
        # display wrong message on the screen
        else:
            font = pygame.font.SysFont('Consolas', 60)
            text = font.render("Špatně!", True, COLOR_RED)
            screen.blit(text, (SCREEN_WIDTH/2-125, SCREEN_HEIGHT/2))

    # If task_id isn't the last in array
    # load next scheme (begin new level)
    if won_the_round and task_id != len(tasks):
        if next_round(screen, mouse, task_id, all_components, tasks):
            all_components.append(multi_meter)
            won_the_round = False

    # If task_id is the last in array
    # end the game (break out of loop)
    elif task_id == len(tasks):
        if end_round(screen, mouse):
            break

    pygame.display.flip()
    pygame.display.update()
pygame.quit()