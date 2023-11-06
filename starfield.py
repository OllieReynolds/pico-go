from picographics import PicoGraphics, DISPLAY_TUFTY_2040
import time
import random

# Initialize display
display = PicoGraphics(display=DISPLAY_TUFTY_2040)
WIDTH, HEIGHT = display.get_bounds()

# Constants
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

# Colors
BLACK = display.create_pen(0, 0, 0)

# Initialize starfield
num_stars = 100
# Stars initialized near the center (x, y, z)
stars = [(random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(1, 5)) for _ in range(num_stars)]

def calculate_brightness(z):
    # Inverse relation between brightness and distance
    brightness = int(255 * (1 - z / 5.0))
    # Add a random factor for twinkling effect
    brightness += random.randint(-20, 20)
    # Clamp the brightness between 0 and 255
    return max(0, min(255, brightness))

# Main loop
while True:
    # Clear the screen
    display.set_pen(BLACK)
    display.rectangle(0, 0, WIDTH, HEIGHT)

    # Update and draw stars
    new_stars = []
    for x, y, z in stars:
        # Simulate movement away from the viewer by increasing the z value
        new_z = z + 0.2

        # Reset star to a new position and depth if it gets too far
        if new_z >= 5:
            new_z = 1.0
            x, y = random.uniform(-5, 5), random.uniform(-5, 5)

        # Project the 3D point to 2D space
        proj_x = int((x / new_z) * (WIDTH // 4) + CENTER_X)
        proj_y = int((y / new_z) * (HEIGHT // 4) + CENTER_Y)

        # Calculate brightness based on z-coordinate
        brightness = calculate_brightness(new_z)
        pen = display.create_pen(brightness, brightness, brightness)

        # Draw the star only if it's inside the screen boundaries
        if 0 <= proj_x < WIDTH and 0 <= proj_y < HEIGHT:
            display.set_pen(pen)
            display.circle(proj_x, proj_y, 2)

        new_stars.append((x, y, new_z))
    stars = new_stars

    # Update display
    display.update()
    
    # Delay for smooth animation
    time.sleep(0.05)
