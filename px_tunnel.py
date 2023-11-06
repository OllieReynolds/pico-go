from picographics import PicoGraphics, DISPLAY_TUFTY_2040
import time
import math

# Initialize display
display = PicoGraphics(display=DISPLAY_TUFTY_2040)
WIDTH, HEIGHT = display.get_bounds()

# Colors
BLACK = display.create_pen(0, 0, 0)

# Initial parameters
num_rectangles = 30
max_size = min(WIDTH, HEIGHT)
step_size = max_size // num_rectangles
angle = 0.0

# Main loop
while True:
    # Clear the screen
    display.set_pen(BLACK)
    display.rectangle(0, 0, WIDTH, HEIGHT)

    # Draw the tunnel
    for i in range(num_rectangles):
        size = max_size - i * step_size
        offset = i * step_size // 2
        color_val = int(255 * (i / num_rectangles))
        color = display.create_pen(color_val, 0, 255 - color_val)
        
        display.set_pen(color)
        
        x = int(WIDTH // 2 + math.cos(angle) * offset) - size // 2
        y = int(HEIGHT // 2 + math.sin(angle) * offset) - size // 2
        display.rectangle(x, y, size, size)
    
    # Update the angle for animation
    angle += 0.1
    
    # Update the display
    display.update()
    
    # Delay for smooth animation
    time.sleep(0.05)
