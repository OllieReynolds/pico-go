# This is a Tufty2040 with VERY limited memory and processing power.
from picographics import PicoGraphics, DISPLAY_TUFTY_2040
import time
import random
import math

display = PicoGraphics(display=DISPLAY_TUFTY_2040)
WIDTH, HEIGHT = display.get_bounds()

loop_time = 0.01

BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
NAVY_BLUE = display.create_pen(0, 0, 100)
MOON_COLOR = display.create_pen(255, 255, 224)
GREEN = display.create_pen(0, 190, 0)
MED_GREEN = display.create_pen(0, 135, 0)
DARK_GREEN = display.create_pen(0, 65, 0)

hill_height = HEIGHT // 4
hill_frequency = 2 * math.pi / WIDTH * 2.0
x_phase = 0
y_phase = HEIGHT // 2
num_rectangles = 60

def draw_hill(display, hill_height, hill_frequency, x_phase, y_phase, num_rectangles, colour):
    rect_width = WIDTH // num_rectangles
    gap = WIDTH % num_rectangles

    display.set_pen(colour)
    
    x = 0
    for i in range(num_rectangles):
        extra_gap = 1 if i < gap else 0
        actual_rect_width = rect_width + extra_gap
        
        y = int(y_phase + hill_height * math.sin(hill_frequency * (x - x_phase)))
        rect_height = HEIGHT - y
        
        display.rectangle(x, y, actual_rect_width, rect_height)
        x += actual_rect_width

def draw_hills():
    t  = time.ticks_ms()
    t1 = t / 10.0
    t2 = t / 20.0
    t3 = t / 30.0
    
    draw_hill(display, hill_height * 0.3, hill_frequency * 0.9, x_phase                           - t3, y_phase - 20, num_rectangles, DARK_GREEN)
    draw_hill(display, hill_height * 0.2, hill_frequency * 0.6, x_phase - (WIDTH * 0.3)           - t2, y_phase + 00, num_rectangles, MED_GREEN)
    draw_hill(display, hill_height * 0.1, hill_frequency * 0.4, x_phase - (WIDTH * 0.3 * 2)       - t1, y_phase + 50, num_rectangles, GREEN)

# Stars
NUM_STARS = 50
stars = [(random.randint(0, WIDTH-1), random.randint(0, (HEIGHT-1) // 2)) for _ in range(NUM_STARS)]
shooting_star_active = False
shooting_star_x = 0
shooting_star_y = 0
shooting_star_vx = 0
shooting_star_vy = 0
TRAIL_LENGTH = 80

def draw_nightsky():
    global shooting_star_active, shooting_star_x, shooting_star_y, shooting_star_vx, shooting_star_vy
    display.set_pen(NAVY_BLUE)
    display.rectangle(0, 0, WIDTH, HEIGHT)

    moon_x, moon_y, moon_radius = WIDTH // 8, HEIGHT // 8, 15
    display.set_pen(MOON_COLOR)
    display.circle(moon_x, moon_y, moon_radius)

    # Draw Stars
    display.set_pen(WHITE)
    for x, y in stars:
        if random.randint(0, 100) > 5:
            display.circle(x, y, 1)

    if shooting_star_active:
        shooting_star_x += shooting_star_vx
        shooting_star_y += shooting_star_vy

        for i in range(TRAIL_LENGTH):
            display.set_pen(WHITE)
            display.circle(int(shooting_star_x - i * shooting_star_vx / TRAIL_LENGTH), 
                           int(shooting_star_y - i * shooting_star_vy / TRAIL_LENGTH), 1)
        
        if shooting_star_x > WIDTH or shooting_star_y > HEIGHT:
            shooting_star_active = False
    else:
        if random.randint(0, 1000) > 975:
            shooting_star_active = True
            shooting_star_x, shooting_star_y = random.randint(0, WIDTH//2), random.randint(0, HEIGHT//4)
            
            angle_deg = random.uniform(-45, 45)
            angle_rad = math.radians(angle_deg)
            
            speed = random.uniform(20, 30)
            shooting_star_vx = speed * math.cos(angle_rad)
            shooting_star_vy = speed * math.sin(angle_rad)
            
frame = 0
speed = 70.5
time_per_frame = 1.0 / speed
time_counter = 0.0
display.set_font("bitmap8") 
display.load_spritesheet("foo.rgb332") 

def draw_fox(x1, x2, x3, y1, y2, position_x, position_y, scale):
    display.sprite(x1, y1, position_x + 0 * 8,         position_y,             scale, BLACK)
    display.sprite(x2, y1, position_x + 1 * 8 * scale, position_y,             scale, BLACK) 
    display.sprite(x3, y1, position_x + 2 * 8 * scale, position_y,             scale, BLACK)
    display.sprite(x1, y2, position_x + 0 * 8,         position_y + 8 * scale, scale, BLACK) 
    display.sprite(x2, y2, position_x + 1 * 8 * scale, position_y + 8 * scale, scale, BLACK) 
    display.sprite(x3, y2, position_x + 2 * 8 * scale, position_y + 8 * scale, scale, BLACK) 

def draw_running_fox():
    global frame, time_counter
    
    scale = 4
    position_x = 160
    position_y = 140
    
    if frame == 0:
        draw_fox(0, 1, 2, 0, 1, position_x, position_y, scale)
    elif frame == 1:
        draw_fox(3, 4, 5, 0, 1, position_x, position_y, scale)
    elif frame == 2:
        draw_fox(6, 7, 8, 0, 1, position_x, position_y, scale)
    elif frame == 3:
        draw_fox(9, 10, 11, 0, 1, position_x, position_y, scale)
    elif frame == 4:
        draw_fox(12, 13, 14, 0, 1, position_x, position_y, scale)
    elif frame == 5:
        draw_fox(0, 1, 2, 2, 3, position_x, position_y, scale)
    elif frame == 6:
        draw_fox(3, 4, 5, 2, 3, position_x, position_y, scale)
    elif frame == 7:
        draw_fox(6, 7, 8, 2, 3, position_x, position_y, scale)

    time_counter += 0.05
    
    if time_counter >= time_per_frame:
        frame += 1
        if frame > 7:
            frame = 0
        time_counter -= time_per_frame

while True:
    draw_nightsky()
    draw_hills()
    draw_running_fox()

    display.update()
    
    time.sleep(loop_time)