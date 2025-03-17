from pyray import *
import math

from modules.colors import COLORS
from modules.graph import *
from modules.gui import Button
from modules.encryption import *

class Player:
    def __init__(self, pos):
        self.pos = pos
        self.radius = 10

        self.color = COLORS.SECONDARY

    def update(self, delta_time: float):
        pass

    def render(self):
        draw_circle_v(self.pos, self.radius, self.color)

class Game:
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        with open("assets/settings", "r") as file:
            settings = eval(decode(file.read()))

        self.btn = Button([200, 200], [100, 100], "test")

        self.drag_start = [0, 0]
        self.drag_end = [0, 0]
        self.drag_vector = [0, 0]
        self.drag_text_pos = [0, 0]
        self.drag_text_pos_off = [5, -5]
        self.is_dragging = False
        self.drag_text_border_size = 5
        self.drag_text_type = settings["game"]["mesure_mode"] # "vector", "length"

        self.own_player = Player([500, 500])

    def update(self, delta_time: float):
        self.btn.update(delta_time)
        mouse_pos = get_mouse_position()

        if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
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

        self.own_player.update(delta_time)

    def render(self):
        for i in range(0, self.WIDTH, 100):
            draw_line(i, 0, i, self.HEIGHT, COLORS.PRIMARY)
            draw_line(0, i, self.WIDTH, i, COLORS.PRIMARY)

        for i in range(0, self.WIDTH, 10):
            draw_line(i, 0, i, self.HEIGHT, [*COLORS.PRIMARY_LIST, 50])
            draw_line(0, i, self.WIDTH, i, [*COLORS.PRIMARY_LIST, 50])

        draw_graph(claculate_graph("sin(x)*100", 0, self.WIDTH, 1), translate=self.own_player.pos)
        self.btn.render()

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

        self.own_player.render()
