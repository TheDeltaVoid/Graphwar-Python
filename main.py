from pyray import *

from modules.colors import COLORS, rgb_to_hsv

from modules.graph import GraphAnim, calculate_graph
from modules.menus import MainMenu, SettingsMenu
from modules.game import Game
from modules.transition import TransitionCircle
from modules.gui import *

WIDTH, HEIGHT = 1080, 720

def main():
    init_window(WIDTH, HEIGHT, "Graphwar Simon-Edition")
    set_exit_key(0)
    set_target_fps(240)

    main_menu = MainMenu(WIDTH, HEIGHT)
    settings_menu = SettingsMenu(WIDTH, HEIGHT)

    game = Game(WIDTH, HEIGHT)

    current = "main"
    next_current = "main"
    last_current = "main"

    in_transition = False
    transition_class = None
    transition_action = ""

    changed = True
    delta_time = 0
    run = True 
    while not window_should_close() and run:
        delta_time = get_frame_time()

        if transition_class != None:
            transition_action = transition_class.update(delta_time)
            if transition_action == "in":
                changed = False

            if transition_action == "hold" and not changed:
                last_current = current
                current = next_current
                changed = True

            elif transition_action == "end":
                transition_class = None

        if current == "quit":
            run = False
            continue

        elif current == "main":
            action = main_menu.update(delta_time)

            if action != "stay" and not in_transition:
                if action == "settings" and transition_class == None:
                    transition_class = TransitionCircle(WIDTH, HEIGHT)
                    next_current = "settings"

                elif action == "host" and transition_class == None:
                    transition_class = TransitionCircle(WIDTH, HEIGHT)
                    next_current = "game"
                    game.reload_settings()

                elif action == "quit" and transition_class == None:
                    transition_class = TransitionCircle(WIDTH, HEIGHT)
                    next_current = "quit"

        elif current == "settings":
            action = settings_menu.update(delta_time, last_current)

            if action != "stay" and transition_class == None:
                transition_class = TransitionCircle(WIDTH, HEIGHT)
                next_current = action

        elif current == "game":
            action = game.update(delta_time)

            if action != "stay" and transition_class == None:
                transition_class = TransitionCircle(WIDTH, HEIGHT)
                next_current = action

        begin_drawing()
        clear_background(COLORS.BG)

        if current == "main":
            main_menu.render()

        elif current == "settings":
            settings_menu.render()

        elif current == "game":
            game.render()

        if transition_class != None:
            transition_class.render()

        draw_fps(5, 5)
        end_drawing()

    close_window()

main()
