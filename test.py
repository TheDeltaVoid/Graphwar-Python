from pyray import *

init_window(1000, 700, "test")

while not window_should_close():
    begin_drawing()
    clear_background(BLACK)

    draw_text("TEST TEXT", 20, 50, 20, WHITE)
    draw_text_ex(get_font_default(), "TEST TEXT", (20, 70), 20, 2.0, WHITE)

    end_drawing()

# spacing is always font_size / 10
