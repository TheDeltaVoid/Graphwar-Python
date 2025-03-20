from pyray import *
import numpy

from modules.colors import COLORS
from modules.encryption import *

def sin(val):
    val = numpy.multiply(val, 1 / 360 * 2 * numpy.pi)
    val = numpy.sin(val)

    return val

def cos(val):
    val = numpy.multiply(val, 1 / 360 * 2 * numpy.pi)
    val = numpy.cos(val)

    return val

def tan(val):
    val = numpy.multiply(val, 1 / 360 * 2 * numpy.pi)
    val = numpy.tan(val)

    return val

def calculate_graph(function: str, start, stop, step) -> list[float, float]:
    function = function.replace(" ", "")
    function = function.replace("^", "**")

    for index, char in enumerate(function):
        if char == "x":
            if index != 0 and function[index - 1] in list("1234567890"):
                chars = list(function)
                chars.insert(index, "*")
                function = "".join(chars)

            if len(function) > index + 1 and function[index + 1] in list("1234567890"):
                chars = list(function)
                chars.insert(index + 1, "*")
                function = "".join(chars)

    print(function)

    x = numpy.linspace(start, stop, int((stop - start) / step))
    y = eval(function, {"x" : x, "sin" : sin, "cos" : cos, "tan" : tan, "sqrt" : numpy.sqrt})

    return [[x_val, y_val] for x_val, y_val in zip(x, y)]

def render_graph(points: list[float, float], translate=[0, 0]):
    translate[0], translate[1] = int(translate[0]), int(translate[1])

    points = [[translate[0] + x, translate[1] - y] for x, y in points]

    draw_line_strip(points, len(points), COLORS.PRIMARY)

def check_collision_graph_circle(points: list[float, float], translate: list[float, float], circle_pos: list[float, float], circle_radius: float) -> bool:
    translate[0], translate[1] = int(translate[0]), int(translate[1])

    last_points = []
    for point in points:
        render_point = [translate[0] + int(point[0]), translate[1] - int(point[1 * -1])]
        last_points.append(render_point)

        if len(last_points) >= 2:
            if check_collision_circle_line(circle_pos, circle_radius, render_point, last_points[-2]):
                return True
        
    return False

class GraphAnim:
    def __init__(self, function, translate=[0, 0], should_disappear=True) -> bool:
        self.initialized = False
        
        with open("assets/settings", "r") as file:
            settings = eval(decode(file.read()))

        self.anim_speed = settings["game"]["graph_anim_speed"]
        self.anim_speed = 0.2
        self.counter = 0

        self.translate = translate

        try:
            self.points = calculate_graph(function, 0, 1080 - translate[0], 1)

        except Exception:
            return
        
        self.points_count = len(self.points)

        self.points_shown = 0

        self.should_disappear = should_disappear
        self.disappear = False
        self.finished = False

        self.initialized = True

    def update(self, delta_time: float):
        if not self.disappear:
            self.counter += delta_time * self.anim_speed

        elif self.should_disappear:
            self.counter -= delta_time * self.anim_speed

        self.counter = min(max(self.counter, 0), 1)

        if self.counter >= 1:
            self.disappear = True

        self.points_shown = int(self.counter * self.points_count)

    def render(self):
        if not self.disappear:
            render_graph(self.points[:self.points_shown], self.translate)

        else:
            render_graph(self.points[self.points_count - self.points_shown:], self.translate)
