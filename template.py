# This is a Tufty2040 with VERY limited memory and processing power.
from picographics import PicoGraphics, DISPLAY_TUFTY_2040
import time

# Initialize display
display = PicoGraphics(display=DISPLAY_TUFTY_2040)
WIDTH, HEIGHT = display.get_bounds()

# Colors
BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)

# Main loop
while True:
    # Clear the screen
    display.set_pen(BLACK)
    display.rectangle(0, 0, WIDTH, HEIGHT)

    # Update display
    display.update()
    
    # Delay for smooth animation
    time.sleep(0.05)