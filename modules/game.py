from pyray import *
import math
import random

from modules.colors import COLORS
from modules.graph import *
from modules.gui import InputBox, Button
from modules.encryption import *
from modules.networking import Server, Client
from modules.player import Player

class Game:
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        with open("assets/settings", "r") as file:
            settings = eval(decode(file.read()))

        self.drag_start = [0, 0]
        self.drag_end = [0, 0]
        self.drag_vector = [0, 0]
        self.drag_text_pos = [0, 0]
        self.drag_text_pos_off = [5, -5]
        self.is_dragging = False
        self.drag_text_border_size = 5
        self.drag_text_type = settings["game"]["mesure_mode"] # "vector", "length"

        self.input_box = InputBox([40, 560], [500, 50])
        self.fire_button = Button([40, 640], [100, 40], "Fire", border_size=20)
        self.clear_button = Button([160, 640], [100, 40], "Clear", border_size=20)
        self.settings_button = Button([920, 565], [120, 40], "Settings", border_size=20)
        self.exit_button = Button([920, 640], [120, 40], "Exit", border_size=20)

        self.control_box = [30, 550, 1020, 150]
        self.control_box_border = 10

        self.control_box_shadow = self.control_box
        self.control_box_shadow[0] -= self.control_box_border
        self.control_box_shadow[1] -= self.control_box_border
        self.control_box_shadow[2] += self.control_box_border * 2
        self.control_box_shadow[3] += self.control_box_border * 2
        
        self.player = Player([0, 0])
        self.other_player = Player([0, 0])

        self.graph_anims: list[GraphAnim] = []

        self.server = None
        self.client = None

        self.turn = "False"

    def reset(self):
        self.server = None
        self.client = None
        self.graph_anims = []

    def set_server(self, server: Server):
        self.client = None
        self.server = server

        self.turn = "True"

        player_pos = [random.randint(50, 400), random.randint(50, 500)]
        other_player_pos = [random.randint(680, 1030), random.randint(50, 500)]

        self.player = Player(player_pos)
        self.other_player = Player(other_player_pos)

        data_string = "DATA_STRING" + "{" + f"'other_player_pos' : {player_pos}, 'player_pos' : {other_player_pos}" + "}"
        self.server.send(data_string)

    def set_client(self, client: Client):
        self.server = None
        self.client = client

        self.turn = "False"

    def recv_callback(self, function):
        if len(function) > 11 and function[:11] == "DATA_STRING":
            data_dict = eval(function[11:])

            player_pos = [540 - (data_dict["player_pos"][0] - 540), data_dict["player_pos"][1]]
            other_player_pos = [540 - (data_dict["other_player_pos"][0] - 540), data_dict["other_player_pos"][1]]

            self.player = Player(player_pos)
            self.other_player = Player(other_player_pos)

        else:
            self.turn = "Next"

            self.add_graph(function, self.other_player, reverse=True)

    def add_graph(self, function, player=None, clear_graphs=True, reverse=False) -> bool:
        if player == None:
            player = self.player

        anim = GraphAnim(function, player.pos, should_disappear=True, reverse=reverse)
        if anim.initialized:
            if clear_graphs:
                self.graph_anims = []

            self.graph_anims.append(anim)
            return True
        
        return False

    def reload_settings(self):
        with open("assets/settings", "r") as file:
            settings = eval(decode(file.read()))

        self.drag_text_type = settings["game"]["mesure_mode"]

        self.player.reload_settings()
        self.other_player.reload_settings()

    def update(self, delta_time: float):
        mouse_pos = get_mouse_position()
        self.input_box.update(delta_time)
        self.player.update(delta_time)
        self.other_player.update(delta_time)

        if len(self.graph_anims) > 0 and self.graph_anims[0].finished:
            if self.turn == "Next":
                self.turn = "True"

        for anim in self.graph_anims:
            anim.update(delta_time)

            if self.turn == "False" or self.turn == "Next":
                if self.player.is_colliding_with_graph(anim):
                    anim.finish()

            elif self.other_player.is_colliding_with_graph(anim):
                anim.finish()

        if self.server != None:
            self.server.update(delta_time)

        elif self.client != None:
            self.client.update(delta_time)

        if (self.fire_button.update(delta_time) or is_key_pressed(KeyboardKey.KEY_ENTER)) and self.turn == "True":
            if self.add_graph(self.input_box.text):
                if self.server != None:
                    self.server.send(self.input_box.text)

                elif self.client != None:
                    self.client.send(self.input_box.text)

                self.turn = False

        if self.clear_button.update(delta_time):
            pass
            #self.graph_anims = []

        if self.settings_button.update(delta_time):
            return "settings"
        
        if self.exit_button.update(delta_time):
            if self.server != None:
                self.server.close()

            if self.client != None:
                self.client.close()

            return "main"

        if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT) and not check_collision_point_rec(mouse_pos, self.control_box):
            self.drag_start[0] = mouse_pos.x
            self.drag_start[1] = mouse_pos.y

            self.is_dragging = True

        elif not is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT):
            self.is_dragging = False

        if self.is_dragging:
            self.drag_end[0] = mouse_pos.x
            self.drag_end[1] = mouse_pos.y

            self.drag_vector[0] = self.drag_end[0] - self.drag_start[0]
            self.drag_vector[1] = (self.drag_end[1] - self.drag_start[1]) * -1

            self.drag_text_pos[0] = self.drag_start[0] + self.drag_vector[0] / 2 + self.drag_text_pos_off[0]
            self.drag_text_pos[1] = self.drag_start[1] + self.drag_vector[1] * -1 / 2 + self.drag_text_pos_off[1]

        return "stay"

    def render(self):
        for i in range(0, self.WIDTH, 100):
            draw_line(i, 0, i, self.HEIGHT, COLORS.PRIMARY)
            draw_line(0, i, self.WIDTH, i, COLORS.PRIMARY)

        for i in range(0, self.WIDTH, 10):
            draw_line(i, 0, i, self.HEIGHT, [*COLORS.PRIMARY_LIST, 50])
            draw_line(0, i, self.WIDTH, i, [*COLORS.PRIMARY_LIST, 50])

        for anim in self.graph_anims:
            anim.render()

        draw_rectangle_rounded(self.control_box, 0.2, 20, COLORS.SECONDARY)
        draw_rectangle_rounded(self.control_box_shadow, 0.2, 20, Color(0, 0, 0, 40))
        
        self.input_box.render()
        self.fire_button.render()
        self.clear_button.render()
        self.settings_button.render()
        self.exit_button.render()

        self.player.render()
        self.other_player.render()

        if self.is_dragging:
            draw_line_ex(self.drag_start, self.drag_end, 1, COLORS.PRIMARY)
            draw_circle(int(self.drag_start[0]), int(self.drag_start[1]), 3, BLACK)

            if self.drag_text_type == "vector":
                text = str(round(self.drag_vector[0], 2)) + " | " + str(round(self.drag_vector[1], 2))

            elif self.drag_text_type == "length":
                text = str(round(math.sqrt(self.drag_vector[0] ** 2 + self.drag_vector[1] ** 2)))

            text_size = measure_text_ex(get_font_default(), text, 20, 2)

            text_rect_pos = [self.drag_text_pos[0] - self.drag_text_border_size, self.drag_text_pos[1] - self.drag_text_border_size]
            text_rect_size = [text_size.x + self.drag_text_border_size * 2, text_size.y + self.drag_text_border_size * 2]

            draw_rectangle_rounded([*text_rect_pos, *text_rect_size], 0.2, 20, COLORS.PRIMARY)
            draw_text(text, int(self.drag_text_pos[0]), int(self.drag_text_pos[1]), 20, BLACK)
