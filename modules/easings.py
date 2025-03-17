import math

def ease(start: float, stop: float, t: float, function):
    if t <= start:
        return start
    
    elif t >= stop:
        return stop

    length = stop - start
    t_normalized = (t - start) / length

    return start + function(t_normalized) * length

def linear(t):
    return t

def ease_in_quad(t):
    return t * t

def ease_out_quad(t):
    return t * (2 - t)

def ease_in_out_quad(t):
    return 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t

def ease_in_cubic(t):
    return t * t * t

def ease_out_cubic(t):
    return (t - 1) ** 3 + 1

def ease_in_out_cubic(t):
    return 4 * t * t * t if t < 0.5 else (t - 1) * (2 * t - 2) * (2 * t - 2) + 1

def ease_in_quart(t):
    return t * t * t * t

def ease_out_quart(t):
    return 1 - (t - 1) ** 4

def ease_in_out_quart(t):
    return 8 * t * t * t * t if t < 0.5 else 1 - 8 * (t - 1) ** 4

def ease_in_quint(t):
    return t ** 5

def ease_out_quint(t):
    return 1 + (t - 1) ** 5

def ease_in_out_quint(t):
    return 16 * t ** 5 if t < 0.5 else 1 + 16 * (t - 1) ** 5

def ease_in_sine(t):
    return 1 - math.cos((t * math.pi) / 2)

def ease_out_sine(t):
    return math.sin((t * math.pi) / 2)

def ease_in_out_sine(t):
    return -(math.cos(math.pi * t) - 1) / 2

def ease_in_expo(t):
    return 0 if t == 0 else 2 ** (10 * (t - 1))

def ease_out_expo(t):
    return 1 if t == 1 else 1 - 2 ** (-10 * t)

def ease_in_out_expo(t):
    if t == 0 or t == 1:
        return t
    return (2 ** (20 * t - 10) / 2) if t < 0.5 else (2 - 2 ** (-20 * t + 10)) / 2

def ease_in_circ(t):
    return 1 - math.sqrt(1 - t * t)

def ease_out_circ(t):
    return math.sqrt(1 - (t - 1) ** 2)

def ease_in_out_circ(t):
    return (1 - math.sqrt(1 - 4 * t * t)) / 2 if t < 0.5 else (math.sqrt(1 - (2 * t - 2) ** 2) + 1) / 2

def ease_in_back(t):
    c1 = 1.70158
    return c1 * t ** 3 - c1 * t ** 2

def ease_out_back(t):
    c1 = 1.70158
    return 1 + c1 * (t - 1) ** 3 + c1 * (t - 1) ** 2

def ease_in_out_back(t):
    c1 = 1.70158 * 1.525
    return ((t * 2) ** 2 * ((c1 + 1) * t * 2 - c1)) / 2 if t < 0.5 else ((t * 2 - 2) ** 2 * ((c1 + 1) * (t * 2 - 2) + c1) + 2) / 2
