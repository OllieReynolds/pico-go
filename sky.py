from picographics import PicoGraphics, DISPLAY_TUFTY_2040, PEN_RGB565, PEN_RGB888, PEN_RGB332  
import time

# Initialize display
display = PicoGraphics(display=DISPLAY_TUFTY_2040, pen_type=PEN_RGB332)
WIDTH, HEIGHT = display.get_bounds()

# Function to perform linear interpolation
def lerp(a, b, t):
    return int((1 - t) * a + t * b)

# Colors
BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
COLORS = [
    [255, 0, 0],  # RED
    [0, 255, 0],  # GREEN
    [0, 0, 255],  # BLUE
    [255, 255, 0] # YELLOW
]

# Full cycle time in seconds
full_cycle_time = 10.0

# Frame delay in seconds
frame_delay = 0.05

# Calculate direction increment based on full cycle time and frame rate
frames_per_second = 1 / frame_delay
direction = 1 / (full_cycle_time * frames_per_second)

# Record the starting time
start_time = time.time()

# Main loop
t = 0.0

while True:
    # Clear the screen
    display.set_pen(BLACK)
    display.rectangle(0, 0, WIDTH, HEIGHT)

    # Determine which segment we're in
    segment = int(t * 4) % 4  # Scale by 4 because there are 4 segments
    next_segment = (segment + 1) % 4
    local_t = (t * 4) % 1  # t within the current segment

    # Interpolate between the colors of the current and next segments
    r = lerp(COLORS[segment][0], COLORS[next_segment][0], local_t)
    g = lerp(COLORS[segment][1], COLORS[next_segment][1], local_t)
    b = lerp(COLORS[segment][2], COLORS[next_segment][2], local_t)

    # Create the interpolated color pen
    interpolated_color = display.create_pen(r, g, b)
    
    # Draw with the interpolated color
    display.set_pen(interpolated_color)
    display.rectangle(10, 10, WIDTH - 20, HEIGHT - 20)

    # Calculate elapsed time based on the starting time
    elapsed_time = time.time() - start_time

    # Draw elapsed time text
    display.set_pen(WHITE)
    display.text("Elapsed Time: {:.2f} s".format(elapsed_time), 10, HEIGHT - 30)

    # Update display
    display.update()

    # Update t for next iteration
    t += direction
    t %= 1.0  # Cycle t back to 0 after it reaches 1, so it aligns with full_cycle_time

    # Delay for smooth animation
    time.sleep(frame_delay)
