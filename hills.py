from picographics import PicoGraphics, DISPLAY_TUFTY_2040
import time
import math

# Initialize display
display = PicoGraphics(display=DISPLAY_TUFTY_2040)
WIDTH, HEIGHT = display.get_bounds()

# Colors
BLACK = display.create_pen(0, 0, 0)
GREEN = display.create_pen(0, 255, 0)
DARK_GREEN = display.create_pen(0, 85, 0)
MED_GREEN = display.create_pen(0, 155, 0)

# Sine wave parameters disguised as hill parameters
hill_height = HEIGHT // 4
hill_frequency = 2 * math.pi / WIDTH * 2.0
x_phase = 0  # Phase shift along x-axis
y_phase = HEIGHT // 2  # Phase shift along y-axis
num_rectangles = 60

def draw_hill(display, hill_height, hill_frequency, x_phase, y_phase, num_rectangles, colour):
    rect_width = WIDTH // num_rectangles  # Width of each rectangle
    gap = WIDTH % num_rectangles

    # Set pen color to green
    display.set_pen(colour)
    
    x = 0
    for i in range(num_rectangles):
        extra_gap = 1 if i < gap else 0  # Distribute the extra pixels
        actual_rect_width = rect_width + extra_gap
        
        y = int(y_phase + hill_height * math.sin(hill_frequency * (x - x_phase)))
        rect_height = HEIGHT - y  # Height of the rectangle
        
        display.rectangle(x, y, actual_rect_width, rect_height)
        x += actual_rect_width  # Move the x position

def draw_hills():
    t  = time.ticks_ms()
    t1 = t / 10.0
    t2 = t / 20.0
    t3 = t / 30.0
    
    # Draw hill and fill it with rectangles
    draw_hill(display, hill_height * 0.3, hill_frequency * 0.9,       x_phase                     + t3, y_phase - 20,       num_rectangles, DARK_GREEN)
    draw_hill(display, hill_height * 0.2, hill_frequency * 0.6, x_phase - (WIDTH * 0.3)           + t2, y_phase + 00,  num_rectangles, MED_GREEN)
    draw_hill(display, hill_height * 0.1, hill_frequency * 0.4, x_phase - (WIDTH * 0.3 * 2)       + t1, y_phase + 50, num_rectangles, GREEN)

# Main loop
while True:
    # Clear the screen
    display.set_pen(BLACK)
    display.rectangle(0, 0, WIDTH, HEIGHT)
    
    draw_hills()
    
    # Update display
    display.update()

    # Delay for smooth animation
    time.sleep(0.05)
