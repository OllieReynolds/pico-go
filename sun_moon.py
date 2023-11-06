from picographics import PicoGraphics, DISPLAY_TUFTY_2040
import time
import math

# Initialize display and other settings
display = PicoGraphics(display=DISPLAY_TUFTY_2040)
WIDTH, HEIGHT = display.get_bounds()

BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
YELLOW = display.create_pen(255, 255, 0)

CYCLE_DURATION = 10

total_distance = 2 * WIDTH

speed = int(total_distance / (CYCLE_DURATION / 0.05))

circle_x = WIDTH
is_sun = True

def draw_circle(display, x, y, is_sun):
    if is_sun:
        circle_radius = 30
        display.set_pen(YELLOW)
    else:
        circle_radius = 15
        display.set_pen(WHITE)
    
    if 0 <= y < HEIGHT:
        display.circle(x, y, circle_radius)
    return circle_radius

def draw_sun_moon():
    global circle_x, is_sun
    
    display.set_pen(WHITE)
    a = 61
    b = 57
    
    circle_y_sine = int(b * math.sin((math.pi * circle_x) / 320) - a)
    circle_y = 7 - circle_y_sine
    
    circle_radius = draw_circle(display, circle_x, circle_y, is_sun)
    
    circle_x -= speed
    
    if circle_x < -circle_radius:
        circle_x = WIDTH + circle_radius
        is_sun = not is_sun

while True:
    display.set_pen(BLACK)
    display.rectangle(0, 0, WIDTH, HEIGHT)

    draw_sun_moon()
    
    display.update()
    
    time.sleep(0.01)
