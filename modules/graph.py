from pyray import *
import math
import functools

from modules.colors import COLORS
from modules.encryption import *

nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
ops = ["+", "-", "*", "/", "^", "(", ")", "s", "c", "t"]
def tokenize(function: str) -> list[str]:
    output = []

    function = function.replace("sin", "s").replace("cos", "c").replace("tan", "t")

    token = ""
    for char in function:
        if char in ops:
            if len(token) > 0:
                if token != "x":
                    output.append(float(token))
                    token = ""

                else:
                    output.append(token)
                    token = ""

            output.append(char)

        elif char in nums or char == "." or char == "x":
            token += char

    if token != "x" and len(token) > 0:
        output.append(float(token))

    elif len(token) > 0:
        output.append(token)

    return output

operators = {"+": 0 , "-" : 0, "*": 1 , "/": 1 , "^" : 2, "**" : 2, "s" : 3, "c" : 3, "t" : 3}
def parse_function(function: str) -> list[str, bool]:
    function.replace(" ", "")
    function = function.lower()

    for index, char in enumerate(function):
        if len(function) - (index + 1) >= 1:
            if char in operators.keys() or index == 0:
                if function[index + 1] in ["+", "-"] or (index == 0 and function[index] in ["+", "-"]):
                    if index == 0:
                        chars = list(function)
                        chars.insert(index + 2, ")")
                        chars.insert(index, "(0")

                    else:
                        chars = list(function)
                        chars.insert(index + 3, ")")
                        chars.insert(index + 1, "(0")

                    function = "".join(chars)

    tokens = tokenize(function)

    output = []
    stack = []
    for token in tokens:
        if type(token) == float or token == "x":
            output.append(str(token) + ",")

        elif token in operators.keys():
            if len(stack) > 0:
                while stack[-1] in operators.keys() and operators[stack[-1]] > operators[token]:
                    operator = stack.pop()
                    output.append(operator + ",")

                    if len(stack) <= 0:
                        break

            stack.append(token)

        elif token == "(":
            stack.append(token)

        elif token == ")":
            while stack[-1] != "(":
                operator = stack.pop()
                output.append(operator + ",")

                if len(stack) <= 0:
                    return "", False
                
            stack.pop()

    stack.reverse()
    for operator in stack:
        output.append(operator + ",")

    output_str = "".join(output)
    output_str = output_str[:-1].replace("^", "**")

    return output_str, True

special_operators = ["s", "c", "t"]
def calculate_function(function: str, x: float, parsed=True) -> float:
    if not parsed:
        parsed_function, sucsess = parse_function(function)

        if not sucsess:
            return 0

    else:
        parsed_function = function

    stack = []

    tokens = parsed_function.split(",")
    for token in tokens:
        if token in operators.keys():
            if token not in special_operators:
                print(token)
                a, b = stack.pop(), stack.pop()
                stack.append(eval(str(b) + token + str(a)))

            else:
                if token == "s":
                    a = stack.pop()
                    stack.append(math.sin(math.radians(a)))

                if token == "c":
                    a = stack.pop()
                    stack.append(math.cos(math.radians(a)))

                if token == "t":
                    a = stack.pop()
                    stack.append(math.tan(math.radians(a)))

        else:
            token = float(eval(token))
            stack.append(token)

    return stack[0]

@functools.cache
def claculate_graph(function: str, start, stop, step) -> list[list[float, float]]:
    parsed_function, sucsess = parse_function(function)

    if not sucsess:
        return []

    output = []
    for x in range(start, stop, step):
        output.append([x, calculate_function(parsed_function, x)])

    return output

def draw_graph(points: list[float, float], translate=[0, 0]):
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
    def __init__(self, function, translate=[0, 0]):
        with open("assets/settings", "r") as file:
            settings = eval(decode(file.read()))

        self.anim_speed = settings["game"]["graph_anim_speed"]
        self.anim_speed = 0.2
        self.counter = 0

        self.translate = translate

        self.points = claculate_graph(function, 0, 1080 - translate[0], 1)
        self.points_count = len(self.points)

        self.points_shown = 0

        self.disappear = False
        self.finished = False

    def update(self, delta_time: float):
        if not self.disappear:
            self.counter += delta_time * self.anim_speed

        else:
            self.counter -= delta_time * self.anim_speed

        self.counter = min(max(self.counter, 0), 1)

        if self.counter >= 1:
            self.disappear = True

        self.points_shown = int(self.counter * self.points_count)

    def render(self):
        if not self.disappear:
            draw_graph(self.points[:self.points_shown], self.translate)

        else:
            draw_graph(self.points[self.points_count - self.points_shown:], self.translate)
