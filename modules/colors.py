from pyray import *
from modules.encryption import *

class Colors:
    def __init__(self):
        with open("assets/settings", "r") as file:
            settings = eval(decode(file.read()))

        self.PRIMARY_LIST = settings["colors"]["PRIMARY"]
        self.SECONDARY_LIST = settings["colors"]["SECONDARY"]
        self.BG_LIST = settings["colors"]["BG"]

        self.PRIMARY = Color(*self.PRIMARY_LIST, 255)
        self.SECONDARY = Color(*self.SECONDARY_LIST, 255)
        self.BG = Color(*self.BG_LIST, 255)

    def set_primary_color(self, color: list[int, int, int]):
        self.PRIMARY_LIST = color[:3]
        self.PRIMARY = Color(*self.PRIMARY_LIST, 255)

    def set_secondary_color(self, color: list[int, int, int]):
        self.SECONDARY_LIST = color[:3]
        self.SECONDARY = Color(*self.SECONDARY_LIST, 255)

    def set_bg_color(self, color: list[int, int, int]):
        self.BG_LIST = color[:3]
        self.BG = Color(*self.BG_LIST, 255)

    def save_to_settings(self):
        with open("assets/settings", "r") as file:
            settings = eval(decode(file.read()))

        settings["colors"]["PRIMARY"] = self.PRIMARY_LIST
        settings["colors"]["SECONDARY"] = self.SECONDARY_LIST
        settings["colors"]["BG"] = self.BG_LIST

        settings_str = str(settings)

        with open("assets/settings", "w") as file:
            file.write(encode(settings_str))

COLORS = Colors()

def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    delta = max_c - min_c

    if delta == 0:
        h = 0
    elif max_c == r:
        h = ((g - b) / delta) % 6
    elif max_c == g:
        h = ((b - r) / delta) + 2
    else:
        h = ((r - g) / delta) + 4
    h = round(h * 60)

    s = 0 if max_c == 0 else delta / max_c

    v = max_c

    return [h, s, v]

def hsv_to_rgb(h, s, v):
    h = h % 360
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    return [round((r + m) * 255), round((g + m) * 255), round((b + m) * 255)]

