from pyray import *
from socket import gethostname

from modules.colors import COLORS, rgb_to_hsv

from modules.menus import MainMenu, SettingsMenu, HostMenu, ConnectMenu
from modules.game import Game
from modules.transition import TransitionCircle
from modules.gui import *
from modules.obstacle import Obstacle

WIDTH, HEIGHT = 1080, 720

def main():
    init_window(WIDTH, HEIGHT, "Graphwar Simon-Edition")
    set_exit_key(0)
    set_target_fps(240)

    game = Game(WIDTH, HEIGHT)

    main_menu = MainMenu(WIDTH, HEIGHT)
    settings_menu = SettingsMenu(WIDTH, HEIGHT)
    host_menu = HostMenu(game.recv_callback)
    connect_menu = ConnectMenu(game.recv_callback)

    current = "main"
    next_current = "main"
    last_current = "main"

    transition_class = None
    transition_action = ""

    client = None
    server = None

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
                if next_current == "game":
                    game.reload_settings()

                if next_current == "host":
                    host_menu.init_server()

                if next_current == "join":
                    connect_menu.init_client()

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

            if action != "stay" and transition_class == None:
                if action == "settings" and transition_class == None:
                    transition_class = TransitionCircle(WIDTH, HEIGHT)
                    next_current = "settings"

                elif action == "host" and transition_class == None:
                    transition_class = TransitionCircle(WIDTH, HEIGHT)
                    next_current = "host"

                elif action == "join" and transition_class == None:
                    transition_class = TransitionCircle(WIDTH, HEIGHT)
                    next_current = "join"

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

        elif current == "host":
            action = host_menu.update(delta_time)

            if action != "stay" and transition_class == None:
                if action == "game":
                    server = host_menu.server
                    game.set_server(server)

                transition_class = TransitionCircle(WIDTH, HEIGHT)
                next_current = action

        elif current == "join" and transition_class == None:
            action = connect_menu.update(delta_time)

            if action != "stay":
                if action == "game":
                    client = connect_menu.client
                    game.set_client(client)

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

        elif current == "host":
            host_menu.render()

        elif current == "join":
            connect_menu.render()

        if transition_class != None:
            transition_class.render()

        draw_fps(5, 5)
        end_drawing()

    close_window()

    if host_menu.server != None:
        host_menu.server.close()

    if connect_menu.client != None:
        connect_menu.client.close()

    if server != None:
        server.close()

    if client != None:
        client.close()

    if game.server != None:
        game.server.close()

    if game.client != None:
        game.client.close()

if __name__ == "__main__":
    main()
