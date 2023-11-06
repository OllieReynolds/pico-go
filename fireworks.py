from picographics import PicoGraphics, DISPLAY_TUFTY_2040
import time
import math
import random

# Initialize display
display = PicoGraphics(display=DISPLAY_TUFTY_2040)
WIDTH, HEIGHT = display.get_bounds()

# Colors
DARKEST = display.create_pen(0, 0, 0)

# Firework properties
PARTICLE_COUNT = 50
particles = []

# Initialize particles
def init_particles(x, y):
    global particles
    particles = []
    for _ in range(PARTICLE_COUNT):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        r = random.randint(128, 255)
        g = random.randint(128, 255)
        b = random.randint(128, 255)
        particles.append([x, y, math.cos(angle) * speed, math.sin(angle) * speed, r, g, b])

# Update particle positions
def update_particles():
    for p in particles:
        p[0] += p[2]  # Update x position
        p[1] += p[3]  # Update y position
        p[4] = max(0, p[4] - 5)  # Decay red
        p[5] = max(0, p[5] - 5)  # Decay green
        p[6] = max(0, p[6] - 5)  # Decay blue

# Draw particles
def draw_particles():
    display.set_pen(DARKEST)
    display.rectangle(0, 0, WIDTH, HEIGHT)
    
    for p in particles:
        pen = display.create_pen(int(p[4]), int(p[5]), int(p[6]))
        display.set_pen(pen)
        display.circle(int(p[0]), int(p[1]), 2)

# Main loop
init_particles(WIDTH // 2, HEIGHT // 2)

while True:
    update_particles()
    draw_particles()
    display.update()
    time.sleep(0.05)

    # Reinitialize particles if they have decayed
    if all(p[4] <= 0 and p[5] <= 0 and p[6] <= 0 for p in particles):
        init_particles(WIDTH // 2, HEIGHT // 2)
