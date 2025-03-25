from pyray import *

from modules.colors import *
from modules.graph import GraphAnim, check_collision_graph_circle

class Player:
    def __init__(self, pos):
        self.pos = pos
        self.radius = 10

        self.color = COLORS.SECONDARY

        self.dead = False
        self.death_anim_counter = 0
        self.death_anim_speed = 1

    def reload_settings(self):
        with open("assets/settings", "r") as file:
            settings = eval(decode(file.read()))

        self.color = Color(*settings["colors"]["SECONDARY"], 255)

    def is_colliding_with_graph(self, graph_anim: GraphAnim, can_die=True) -> bool:
        points = graph_anim.points[:graph_anim.points_shown]
        translate = graph_anim.translate

        colliding = check_collision_graph_circle(points, translate, self.pos, self.radius)

        if colliding and can_die:
            self.dead = True

        return colliding

    def update(self, delta_time: float):
        if self.dead:
            self.death_anim_counter += delta_time * self.death_anim_speed

            self.death_anim_counter = min(max(self.death_anim_counter, 0), 1)

            opacity = (1 - self.death_anim_counter) * 255
            self.color.a = int(opacity)

    def render(self):
        draw_circle_v(self.pos, self.radius, self.color)
        