from pyray import *
import math

from modules.colors import COLORS
from modules.easings import *

TRANSITION_DUR_IN = 0.4
TRANSITION_DUR_HOLD = 0.1
TRANSITION_DUR_OUT = 0.4

class TransitionCircle:
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.counter = 0
        self.outer_radius = math.sqrt(WIDTH ** 2 + HEIGHT ** 2)

        self.ease_in_function = ease_out_circ
        self.ease_out_function = ease_in_circ

    def update(self, delta_time: float) -> str:
        self.counter += delta_time

        if self.counter < TRANSITION_DUR_IN:
            return "in"

        elif self.counter < TRANSITION_DUR_IN + TRANSITION_DUR_HOLD:
            return "hold"

        elif self.counter < TRANSITION_DUR_IN + TRANSITION_DUR_HOLD + TRANSITION_DUR_OUT:
            return "out"
        
        else:
            return "end"

    def render(self):
            if self.counter < TRANSITION_DUR_IN:
                inner_radius = self.WIDTH - self.ease_in_function(self.counter / TRANSITION_DUR_IN) * self.WIDTH
                draw_ring([self.WIDTH / 2, self.HEIGHT / 2], inner_radius, self.outer_radius, 0, 360, 100, COLORS.PRIMARY)

            elif self.counter < TRANSITION_DUR_IN + TRANSITION_DUR_HOLD:
                draw_rectangle(0, 0, self.WIDTH, self.HEIGHT, COLORS.PRIMARY)

            elif self.counter < TRANSITION_DUR_IN + TRANSITION_DUR_HOLD + TRANSITION_DUR_OUT:
                inner_radius = self.ease_out_function((self.counter - TRANSITION_DUR_IN - TRANSITION_DUR_HOLD) / TRANSITION_DUR_OUT) * self.WIDTH
                draw_ring([self.WIDTH / 2, self.HEIGHT / 2], inner_radius, self.outer_radius, 0, 360, 100, COLORS.PRIMARY)
