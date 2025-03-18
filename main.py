from pyray import *

from modules.colors import COLORS, rgb_to_hsv

from modules.graph import GraphAnim, claculate_graph
from modules.menus import MainMenu, SettingsMenu
from modules.game import Game
from modules.transition import TransitionCircle
from modules.gui import *

WIDTH, HEIGHT = 1080, 720

claculate_graph("sin(x+5)", 0, 100, 1)

def main():
    init_window(WIDTH, HEIGHT, "Graphwar Simon-Edition")
    set_exit_key(0)
    set_target_fps(240)

    main_menu = MainMenu(WIDTH, HEIGHT)
    settings_menu = SettingsMenu(WIDTH, HEIGHT)

    game = Game(WIDTH, HEIGHT)

    test = GraphAnim("x*0.5", [0, HEIGHT / 2])

    current = "main"
    next_current = "main"

    in_transition = False
    transition_class = None
    transition_action = ""

    delta_time = 0
    run = True
    while not window_should_close() and run:
        delta_time = get_frame_time()

        if transition_class != None:
            transition_action = transition_class.update(delta_time)

            if transition_action == "hold":
                current = next_current

            elif transition_action == "end":
                transition_class = None

        if current == "quit":
            run = False
            continue

        elif current == "main":
            action = main_menu.update(delta_time)

            if action != "stay" and not in_transition:
                if action == "settings":
                    transition_class = TransitionCircle(WIDTH, HEIGHT)
                    next_current = "settings"

                elif action == "host":
                    transition_class = TransitionCircle(WIDTH, HEIGHT)
                    next_current = "game"
                    game.reload_settings()

                elif action == "quit":
                    transition_class = TransitionCircle(WIDTH, HEIGHT)
                    next_current = "quit"

        elif current == "settings":
            action = settings_menu.update(delta_time)

            if action != "stay":
                if action == "main":
                    transition_class = TransitionCircle(WIDTH, HEIGHT)
                    next_current = "main"

        elif current == "game":
            game.update(delta_time)
            test.update(delta_time)

        begin_drawing()
        clear_background(COLORS.BG)

        if current == "main":
            main_menu.render()

        elif current == "settings":
            settings_menu.render()

        elif current == "game":
            game.render()
            test.render()

        if transition_class != None:
            transition_class.render()

        draw_fps(5, 5)
        end_drawing()

    close_window()

main()
