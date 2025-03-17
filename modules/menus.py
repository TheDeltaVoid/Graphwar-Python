from pyray import *
from modules.colors import COLORS

from modules.gui import Button, ToggleButton, ColorPicker

class MainMenu:
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.main_text = "Graphwar"
        self.main_text_size = 100
        self.main_text_spacing = 30

        text_size = measure_text_ex(get_font_default(), self.main_text, self.main_text_size, self.main_text_spacing)
        self.main_text_pos = [WIDTH / 2 - text_size.x / 2, 100]

        self.button_size = [200, 30]
        button_spacing = (WIDTH - 3 * self.button_size[0]) / 4

        self.host_button = Button([button_spacing, 400], self.button_size, "Host Game")
        self.join_button = Button([button_spacing * 2 + self.button_size[0], 400], self.button_size, "Join Game")
        self.settings_button = Button([button_spacing * 3 + self.button_size[0] * 2, 400], self.button_size, "Settings")
        self.quit_button = Button([button_spacing * 2 + self.button_size[0], 600], self.button_size, "Quit")

    def update(self, delta_time: float) -> str:
        if self.host_button.update(delta_time):
            return "host"
        
        if self.join_button.update(delta_time):
            return "join"
        
        if self.settings_button.update(delta_time):
            return "settings"
        
        if self.quit_button.update(delta_time):
            return "quit"

        return "stay"

    def render(self):
        draw_text_ex(get_font_default(), "Graphwar", self.main_text_pos, self.main_text_size, self.main_text_spacing, COLORS.PRIMARY)

        self.host_button.render()
        self.join_button.render()
        self.settings_button.render()
        self.quit_button.render()

class SettingsMenu:
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.back_button = Button([50, 50], [100, 30], "Back", border_size=30)
        self.save_button = Button([210, 50], [100, 30], "Save", border_size=30)

        self.color_picker_primary = ColorPicker([800, 100], COLORS.PRIMARY_LIST)
        self.color_picker_secondary = ColorPicker([800, 300], COLORS.SECONDARY_LIST)
        self.color_picker_bg = ColorPicker([800, 500], COLORS.BG_LIST)

        self.btn = ToggleButton([100, 300], [100, 30], ["Test 1", "Test 2", "Test 3"], border_size=30)

    def update(self, delta_time: float):
        self.color_picker_primary.update(delta_time)
        self.color_picker_secondary.update(delta_time)
        self.color_picker_bg.update(delta_time)

        if self.save_button.update(delta_time):
            COLORS.set_primary_color(self.color_picker_primary.get_color())
            COLORS.set_secondary_color(self.color_picker_secondary.get_color())
            COLORS.set_bg_color(self.color_picker_bg.get_color())
            COLORS.save_to_settings()

        self.btn.update(delta_time)

        if self.back_button.update(delta_time):
            return "main"
        
        return "stay"

    def render(self):
        self.back_button.render()
        self.save_button.render()
        self.btn.render()

        self.color_picker_primary.render()
        self.color_picker_secondary.render()
        self.color_picker_bg.render()
