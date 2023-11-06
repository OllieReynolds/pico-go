from picographics import PicoGraphics, DISPLAY_TUFTY_2040
import time
import math

# Initialize display
display = PicoGraphics(display=DISPLAY_TUFTY_2040)
WIDTH, HEIGHT = display.get_bounds()

# Colors
BLACK = display.create_pen(0, 0, 0)
WHITE1 = display.create_pen(255, 255, 255)
WHITE2 = display.create_pen(200, 200, 200)
WHITE3 = display.create_pen(155, 155, 155)

# Helper Functions
def fract(x):
    return x - math.floor(x)

def rand(x, seed):
    return fract(seed * math.sin(x))

def randStep(x, seed):
    return rand(math.floor(x), seed)

def smoothstep(x):
    return x ** 2 * (1 - 2 * (x - 1))

def smoothsaw(x):
    return smoothstep(fract(x))

def noise(x, seed):
    return randStep(x, seed) * smoothsaw(x) + randStep(x - 1, seed) * (1 - smoothsaw(x - 1))

# Function to quantize the signal
def quantize_signal(value, levels):
    quantized_value = round((levels - 1) * value) / (levels - 1)
    return quantized_value

# Initialize offset for scrolling
offset = 0.0

# Frequency reduction factor
freq_reduction = 0.75

# Initialize previous y_pixel
prev_y_pixel = None

# Function to draw and fill underneath the waveform
def draw_waveform(display, num_rectangles, offset, freq_reduction, colour, seed, y_offest=0):
    rect_width = WIDTH // num_rectangles  # Width of each rectangle
    gap = WIDTH % num_rectangles
    
    display.set_pen(colour)
    
    x = 0
    for i in range(num_rectangles):
        extra_gap = 1 if i < gap else 0  # Distribute the extra pixels
        actual_rect_width = rect_width + extra_gap

        # Calculate the average x_pixel for this rectangle
        avg_x_pixel = x + actual_rect_width // 2

        # Calculate y_pixel for this average x_pixel
        avg_x = (avg_x_pixel + offset) * freq_reduction / 50
        avg_y = noise(avg_x, seed)

        # Quantize the signal
        avg_y_quantized = quantize_signal(avg_y, 64)

        # Scale the amplitude
        avg_y_amplitude_scaled = avg_y_quantized * 0.2

        # Scale and shift y to fit in the display
        avg_y_pixel = int(HEIGHT - (avg_y_amplitude_scaled * HEIGHT)) - y_offest

        # Draw the rectangle
        rect_height = HEIGHT - avg_y_pixel

        display.rectangle(x, avg_y_pixel, actual_rect_width, rect_height)

        x += actual_rect_width  # Move the x position

# Main loop
while True:
    # Clear the screen
    display.set_pen(BLACK)
    display.rectangle(0, 0, WIDTH, HEIGHT)

    y_offset = -20
    draw_waveform(display, 60, offset * 0.25, freq_reduction, WHITE3, 387, 175 + y_offset)
    draw_waveform(display, 60, offset * 0.5, freq_reduction, WHITE2, 698,  125 + y_offset)
    draw_waveform(display, 60, offset * 1.0, freq_reduction, WHITE1, 999,  100 + y_offset)



    # Update display
    display.update()

    offset -= 7.0

    # Delay for smooth animation
    time.sleep(0.016)
