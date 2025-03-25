from pyray import *
import math

from modules.graph import where_collision_graph_circle

def line_circle_intersection(circle, radius, A, B):
    """ Berechnet die Schnittpunkte einer Linie mit einem Kreis. """
    A[1] *= -1
    B[1] *= -1

    cx, cy = circle  # Mittelpunkt des Kreises
    ax, ay = A
    bx, by = B

    # Richtungsvektor der Linie
    dx, dy = bx - ax, by - ay

    # Quadratische Gleichung für Schnittpunkte
    a = dx**2 + dy**2
    b = 2 * (dx * (ax - cx) + dy * (ay - cy))
    c = (ax - cx)**2 + (ay - cy)**2 - radius**2

    # Berechnung der Diskriminante
    disc = b**2 - 4 * a * c

    if disc < 0:
        return []  # Keine Schnittpunkte

    sqrt_disc = math.sqrt(disc)
    t1 = (-b - sqrt_disc) / (2 * a)
    t2 = (-b + sqrt_disc) / (2 * a)

    points = []
    for t in (t1, t2):
        if 0 <= t <= 1:  # Punkt muss auf dem Liniensegment liegen
            intersection = [ax + t * dx, ay + t * dy]
            points.append(intersection)

    return points

class Obstacle:
    def __init__(self, pos, radius, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.pos = pos
        self.radius = radius

        self.color = BLACK

        self.holes = []

    def is_colliding(self, points, translate, take_hit=True):
        collision_index = where_collision_graph_circle(points, translate, self.pos, self.radius)

        if collision_index != -1:
            coll_line = [points[collision_index], points[collision_index - 1]]

            coll_point = line_circle_intersection(self.pos, self.radius, coll_line[0], coll_line[1])

            if coll_point != None:
                self.hit(coll_point[0])
                return True
            
        return False

    def hit(self, pos, size=30):
        self.holes.append([*pos, size])

    def update(self, delta_time: float):
        pass

    def render(self):
        draw_circle(*self.pos, self.radius, self.color)

        for x, y, r in self.holes:
            draw_circle(int(x), int(y), int(r), RED)
