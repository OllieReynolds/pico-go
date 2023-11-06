from picographics import PicoGraphics, DISPLAY_TUFTY_2040
import time

loop_time = 0.005

# Initialize display
display = PicoGraphics(display=DISPLAY_TUFTY_2040)

# set up constants for drawing 
WIDTH, HEIGHT = display.get_bounds() 

BLACK = display.create_pen(0, 0, 0) 
WHITE = display.create_pen(255, 255, 255) 

frame = 0
speed = 70.5  # Higher value = faster animation
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
    
    scale = 8
    position_x = 0
    position_y = 0
    
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
    display.set_pen(BLACK) 
    display.clear()

    draw_running_fox()

    display.update()
    time.sleep(loop_time)
