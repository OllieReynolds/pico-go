from picographics import PicoGraphics, DISPLAY_TUFTY_2040
import time
import random
import math

# Initialize display
display = PicoGraphics(display=DISPLAY_TUFTY_2040)
WIDTH, HEIGHT = display.get_bounds()

# Colors
BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
NAVY_BLUE = display.create_pen(0, 0, 100)
MOON_COLOR = display.create_pen(255, 255, 224)

# Parameters
NUM_STARS = 50
stars = [(random.randint(0, WIDTH-1), random.randint(0, (HEIGHT-1) // 2)) for _ in range(NUM_STARS)]

# Shooting star variables
shooting_star_active = False
shooting_star_x = 0
shooting_star_y = 0
shooting_star_vx = 0
shooting_star_vy = 0
TRAIL_LENGTH = 80

def draw_nightsky():
    global shooting_star_active, shooting_star_x, shooting_star_y, shooting_star_vx, shooting_star_vy
    
    # Clear the screen with navy blue
    display.set_pen(NAVY_BLUE)
    display.rectangle(0, 0, WIDTH, HEIGHT)

    # Draw Moon
    moon_x, moon_y, moon_radius = WIDTH // 8, HEIGHT // 8, 15
    display.set_pen(MOON_COLOR)
    display.circle(moon_x, moon_y, moon_radius)

    # Draw Stars
    display.set_pen(WHITE)
    for x, y in stars:
        if random.randint(0, 100) > 5:  # 95% chance of drawing the star
            display.circle(x, y, 1)

    # Handle Shooting Stars
    if shooting_star_active:
        # Update position based on velocity
        shooting_star_x += shooting_star_vx
        shooting_star_y += shooting_star_vy

        # Draw the shooting star with a trail
        for i in range(TRAIL_LENGTH):
            display.set_pen(WHITE)
            display.circle(int(shooting_star_x - i * shooting_star_vx / TRAIL_LENGTH), 
                           int(shooting_star_y - i * shooting_star_vy / TRAIL_LENGTH), 1)
        
        # Check if shooting star is out of bounds
        if shooting_star_x > WIDTH or shooting_star_y > HEIGHT:
            shooting_star_active = False
    else:
        # 0.5% chance of a new shooting star
        if random.randint(0, 1000) > 990:
            shooting_star_active = True
            shooting_star_x, shooting_star_y = random.randint(0, WIDTH//2), random.randint(0, HEIGHT//4)
            
            # Generate a random angle between -45 and +45 degrees
            angle_deg = random.uniform(-45, 45)
            angle_rad = math.radians(angle_deg)
            
            # Calculate the components of the velocity
            speed = random.uniform(20, 30)
            shooting_star_vx = speed * math.cos(angle_rad)
            shooting_star_vy = speed * math.sin(angle_rad)

# Main loop
while True:
    draw_nightsky()

    # Update display
    display.update()
    
    # Delay for smooth animation
    time.sleep(0.05)
