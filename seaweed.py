from picographics import PicoGraphics, DISPLAY_TUFTY_2040
import time
import math
import urandom as random

display = PicoGraphics(display=DISPLAY_TUFTY_2040)
WIDTH, HEIGHT = display.get_bounds()

BLACK = display.create_pen(0, 0, 0)
SEA_COLOR = display.create_pen(0, 0, 128)  # Darker blue for the sea
DARK_GREEN = display.create_pen(0, 100, 0)  # Darker green for the seaweed

# Initialize empty seaweed list
seaweed = []

def create_clump(x_position):
    clump_size = random.randint(5, 10)  # Number of seaweeds in a clump, increased for density
    for i in range(clump_size):
        # Reduced variation in x position within the clump for denser grouping
        x_var = x_position + random.uniform(-5, 5)
        seaweed.append({
            'x': x_var, 
            'y': HEIGHT, 
            'height': random.randint(30, 70), 
            'width': random.randint(3, 8),
            'sway_offset': random.uniform(-1.0, 1.0),
            'angle_offset': random.uniform(0, math.pi * 2),
        })

# Create initial clumps of seaweed
x_pos = -20
while x_pos < WIDTH + 20:
    create_clump(x_pos)
    # Increased gap between clumps for more distinct clumping
    x_pos += random.randint(40, 120)

# Initialize seaweed with random sway offsets, angles, and widths
seaweed = [{
    'x': x, 
    'y': HEIGHT, 
    'height': random.randint(30, 70), 
    'width': random.randint(3, 8),  # Width variation
    'sway_offset': random.uniform(-1.0, 1.0),
    'angle_offset': random.uniform(0, math.pi * 2),
} for x in range(-20, WIDTH + 20, random.randint(15, 40))]  # Vary the spacing

def draw_seaweed():
    for weed in seaweed:
        sway = weed['sway_offset'] + math.sin(time.ticks_ms() / 1000 * 3 + weed['angle_offset']) * 5
        last_x, last_y = weed['x'], HEIGHT
        for segment in range(0, weed['height'], 2):
            angle = sway * math.sin(segment * 0.1 + weed['angle_offset'])
            segment_x = weed['x'] + angle + random.uniform(-1, 1)  # Jaggedness
            segment_y = HEIGHT - segment + random.uniform(-1, 1)  # Jaggedness
            if 0 <= segment_x < WIDTH:
                # Draw a line from the last segment to the current to create a rough edge
                display.line(int(last_x), int(last_y), int(segment_x), int(segment_y), weed['width'])
            last_x, last_y = segment_x, segment_y

def update_seaweed():
    # Move seaweed to the left to simulate scrolling
    for weed in seaweed:
        weed['x'] -= 1

    # If a seaweed has moved off the screen to the left, remove it
    seaweed[:] = [weed for weed in seaweed if weed['x'] + weed['width'] > -20]

    # Add a new seaweed at the right edge to maintain the number of seaweeds
    if not seaweed or seaweed[-1]['x'] < WIDTH - 20:
        seaweed.append({
            'x': WIDTH + 20, 
            'y': HEIGHT, 
            'height': random.randint(30, 70), 
            'width': random.randint(3, 8),
            'sway_offset': random.uniform(-1.0, 1.0),
            'angle_offset': random.uniform(0, math.pi * 2),
        })

# Main loop
while True:
    display.set_pen(BLACK)
    display.clear()

    display.set_pen(SEA_COLOR)
    display.rectangle(0, 0, WIDTH, HEIGHT)

    display.set_pen(DARK_GREEN)
    draw_seaweed()

    update_seaweed()

    display.update()
    
    time.sleep(0.01)
