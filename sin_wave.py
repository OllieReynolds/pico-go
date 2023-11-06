from picographics import PicoGraphics, DISPLAY_TUFTY_2040
from math import sin, pi
import time

# Initialize display
display = PicoGraphics(display=DISPLAY_TUFTY_2040)
WIDTH, HEIGHT = display.get_bounds()

# Colors
BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
RED = display.create_pen(255, 0, 0)

# Function to plot sine wave and squares
def plot_sine_and_squares(num_squares):
    # Clear the screen
    display.set_pen(BLACK)
    display.rectangle(0, 0, WIDTH, HEIGHT)

    # Set pen to white for sine wave
    display.set_pen(WHITE)

    # Initialize variables
    x_min, x_max = 0, 2 * pi
    error_tolerance = (x_max - x_min) / num_squares
    scale_x = WIDTH / (x_max - x_min)
    scale_y = HEIGHT // 2

    # Draw sine wave
    for x in range(WIDTH):
        y = int(sin(x / scale_x) * scale_y + HEIGHT // 2)
        display.pixel(x, y)

    # Set pen to red for squares
    display.set_pen(RED)

    # Draw squares
    x = x_min
    for _ in range(num_squares):
        x_middle = x + error_tolerance / 2
        min_height = sin(x_middle)
        if min_height > 0:
            square_side = int(min_height * scale_y)
            x_start = int(x * scale_x)
            y_start = HEIGHT - square_side  # Start from the bottom of the screen
            display.rectangle(x_start, y_start, int(error_tolerance * scale_x), square_side)
        x += error_tolerance

# Main loop
while True:
    plot_sine_and_squares(40)

    # Update display
    display.update()

    # Delay for smooth animation
    time.sleep(0.05)
