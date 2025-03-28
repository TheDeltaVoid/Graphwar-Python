from pyray import *

from modules.colors import COLORS, hsv_to_rgb, rgb_to_hsv
from modules.easings import ease, ease_out_quint

from pyray import *
import math

class InputBox:
    def __init__(self, pos, size, always_selected=False):
        self.pos = pos
        self.size = size

        self.text = ""

        self.always_selected = always_selected

        self.text_padding = 10
        self.text_pos = [self.pos[0] + self.text_padding, 0]

        self.insert_index = 0
        self.insert_pos = 0
        self.insert_size = [5, 0]

        self.font_size = 30

        self.backspace_hold = True
        self.backspace_counter = 0
        self.initial_delay = 0.5
        self.repeat_delay = 0.033

    def on_backspace_press(self):
        if self.insert_index == 0:
            return
        
        chars = list(self.text)
        if len(self.text) > 0 and self.insert_index - 1 < len(self.text):
            chars.pop(self.insert_index - 1)

        self.text = "".join(chars)
        self.insert_index -= 1

        self.insert_index = max(0, self.insert_index)

    def update(self, delta_time: float):
        keys = []
        key = get_char_pressed()
        if key != 0:
            while key != 0:
                keys.append(key)
                key = get_char_pressed()

        for key in keys:
            chars = list(self.text)
            chars.insert(self.insert_index, chr(key))
            self.text = "".join(chars)
            self.backspace_hold = False
            self.insert_index += 1

        if is_key_pressed(KeyboardKey.KEY_RIGHT):
            self.insert_index += 1

        if is_key_pressed(KeyboardKey.KEY_LEFT):
            self.insert_index -= 1

        self.insert_index = min(max(self.insert_index, 0), len(self.text))

        if is_key_pressed(KeyboardKey.KEY_BACKSPACE):
            self.on_backspace_press()

        if is_key_released(KeyboardKey.KEY_BACKSPACE):
            self.backspace_hold = False
            self.backspace_counter = 0

        if is_key_down(KeyboardKey.KEY_BACKSPACE):
            self.backspace_counter += delta_time

            if self.backspace_hold:
                if self.backspace_counter >= self.repeat_delay:
                    self.backspace_counter -= self.repeat_delay
                    self.on_backspace_press()

            elif self.backspace_counter >= self.initial_delay:
                self.backspace_counter -= self.initial_delay
                self.backspace_hold = True
                self.on_backspace_press()

        text_size = measure_text_ex(get_font_default(), self.text, self.font_size, self.font_size / 10)
        self.text_pos[1] = self.pos[1] + ( self.size[1] / 2 - text_size.y / 2)

        insert_text_size = measure_text_ex(get_font_default(), self.text[:self.insert_index], self.font_size, self.font_size / 10)
        self.insert_pos = insert_text_size.x + self.pos[0] + self.text_padding + 2

        self.insert_size[1] = text_size.y

    def render(self):
        draw_rectangle_rounded([*self.pos, *self.size], 0.2, 20, COLORS.PRIMARY)
        draw_text(self.text, int(self.text_pos[0]), int(self.text_pos[1]), int(self.font_size), BLACK)

        draw_rectangle_rec([self.insert_pos, self.text_pos[1], *self.insert_size], BLACK)

class Slider:
    def __init__(self, pos, start=0, stop=1, value=0):
        self.pos = pos
        self.size = [100, 10]

        self.start = start
        self.stop = stop

        self.value = value
        self.knob_pos = self.value * self.size[0]
        self.knob_radius = 10

        self.is_dragging = False

        self.select_rect = [self.pos[0], self.pos[1] - (self.knob_radius * 2 - self.size[1]) / 2, self.size[0], self.size[1] + (self.knob_radius * 2 - self.size[1])]

    def get_scaled_value(self) -> float:
        return self.value * (self.stop - self.start) + self.start

    def get_value(self) -> float:
        return self.value

    def update(self, delta_time: float) -> float:
        mouse_pos = get_mouse_position()

        if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT) and check_collision_point_rec(mouse_pos, self.select_rect):
            self.is_dragging = True

        elif is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT) and check_collision_point_circle(mouse_pos, [self.knob_pos + self.pos[0], self.pos[1] + self.size[1] / 2], self.knob_radius + 2):
            self.is_dragging = True

        if is_mouse_button_released(MouseButton.MOUSE_BUTTON_LEFT):
            self.is_dragging = False

        if self.is_dragging:
            pos_on_slider = min(max(mouse_pos.x - self.pos[0], 0), self.size[0])
            self.value = pos_on_slider / self.size[0]
            self.knob_pos = self.value * self.size[0]

    def render(self):
        draw_rectangle_rounded([*self.pos, *self.size], 1.0, 20, COLORS.PRIMARY)
        draw_circle_v([self.knob_pos + self.pos[0], self.pos[1] + self.size[1] / 2], self.knob_radius, BLACK)

class ColorPicker:
    def __init__(self, pos, color=[0, 0, 0]):
        self.pos = pos
        self.size = [140, 150]

        self.color = rgb_to_hsv(*color[:3])

        self.color_field_pos = [self.pos[0] + 10, self.pos[1] + 10]
        self.color_field_size = [self.size[0] - 20, 40]

        self.hue_slider = Slider([self.pos[0] + 20, self.pos[1] + 60], 0, 360, self.color[0] / 360)
        self.saturation_slider = Slider([self.pos[0] + 20, self.pos[1] + 90], 0, 1, self.color[1])
        self.value_slider = Slider([self.pos[0] + 20, self.pos[1] + 120], 0, 1, self.color[2])

    def get_color(self) -> list[int, int, int]:
        return [*hsv_to_rgb(*self.color), 255]

    def update(self, delta_time: float) -> list[int, int, int]:
        self.hue_slider.update(delta_time)
        self.color[0] = self.hue_slider.get_scaled_value()

        self.saturation_slider.update(delta_time)
        self.color[1] = self.saturation_slider.get_scaled_value()

        self.value_slider.update(delta_time)
        self.color[2] = self.value_slider.get_scaled_value()

    def render(self):
        draw_rectangle_rounded([*self.pos, *self.size], 0.2, 20, COLORS.SECONDARY)

        draw_rectangle_rounded([*self.color_field_pos, *self.color_field_size], 0.2, 20, color_from_hsv(*self.color))

        self.hue_slider.render()
        self.saturation_slider.render()
        self.value_slider.render()

class Button:
    def __init__(self, pos: list[float, float], size: list[float, float], text: str, border_size=100):
        self.pos = pos
        self.size = size

        self.border_size = border_size
        self.border_anim_dur = 0.5

        self.roundness = 0.2

        self.font_size = 30
        self.text = text
        self.text_size = measure_text_ex(get_font_default(), self.text, self.font_size, 1.0)
        self.text_pos = [self.pos[0] + self.size[0] / 2 - self.text_size.x / 2, self.pos[1] + self.size[1] / 2 - self.text_size.y / 2]

        self.hover = False
        self.current_border_size = 0
        self.border_counter = 0

        self.expand_ease_func = ease_out_quint
        self.retract_ease_func = ease_out_quint

    def change_text(self, new_text):
        self.text = new_text

        self.text_size = measure_text_ex(get_font_default(), self.text, self.font_size, 1.0)
        self.text_pos = [self.pos[0] + self.size[0] / 2 - self.text_size.x / 2, self.pos[1] + self.size[1] / 2 - self.text_size.y / 2]

    def update(self, delta_time: float) -> bool:
        mouse_pos = get_mouse_position()

        if check_collision_point_rec(mouse_pos, [*self.pos, *self.size]) or (self.hover and check_collision_point_rec(mouse_pos, [*self.border_render_pos, *self.border_render_size])):
            self.hover = True

            self.border_counter += delta_time
            self.border_counter = min(self.border_anim_dur, self.border_counter)

            self.current_border_size = ease(0, self.border_size, self.border_counter / self.border_anim_dur * self.border_size, self.expand_ease_func)            

        elif self.current_border_size > 0:
            self.hover = False

            self.border_counter -= delta_time

            self.current_border_size = ease(0, self.border_size, self.border_counter / self.border_anim_dur * self.border_size, self.retract_ease_func)

        self.border_render_pos = [self.pos[0] - self.current_border_size / 2, self.pos[1] - self.current_border_size / 2]
        self.border_render_size = [self.size[0] + self.current_border_size, self.size[1] + self.current_border_size]

        if self.hover and is_mouse_button_released(MouseButton.MOUSE_BUTTON_LEFT):
            return True
        
        return False

    def render(self):
        if self.current_border_size > 0:
            draw_rectangle_rounded([*self.border_render_pos, *self.border_render_size], self.roundness, 20, COLORS.PRIMARY)

        draw_rectangle_rounded([*self.pos, *self.size], self.roundness, 20, COLORS.PRIMARY)
        draw_text_ex(get_font_default(), self.text, [*self.text_pos], self.font_size, 1.0, BLACK)

class ToggleButton(Button):
    def __init__(self, pos, size, texts, border_size=100, index=0):
        self.texts = texts
        self.index = index

        super().__init__(pos, size, self.texts[self.index], border_size)

    def update(self, delta_time: float):
        pressed = super().update(delta_time)

        if pressed:
            self.index += 1
            self.index %= len(self.texts)

            self.change_text(self.texts[self.index])
    
    def render(self):
        return super().render()
