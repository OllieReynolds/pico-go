import math
import time
from picographics import PicoGraphics, DISPLAY_TUFTY_2040

# Initialize
display = PicoGraphics(display=DISPLAY_TUFTY_2040)

WHITE = display.create_pen(204, 85, 0)

# Function to project 3D point to 2D
def project_3d_to_2d(x, y, z, f, d, center_x, center_y):
    factor = f / (z + d)
    return center_x + factor * x, center_y + factor * y

# Function to compute shading based on depth
def compute_shade(z, min_z, max_z, min_shade, max_shade):
    return max_shade - (z - min_z) / (max_z - min_z) * (max_shade - min_shade)



# Function to rotate a point in 3D space
def rotate_point(x, y, z, ax, ay, az):
    sin_ax, cos_ax = math.sin(ax), math.cos(ax)
    sin_ay, cos_ay = math.sin(ay), math.cos(ay)
    sin_az, cos_az = math.sin(az), math.cos(az)
    
    x_rot = (x * cos_az - y * sin_az) * cos_ay + z * (cos_ax * sin_ay + sin_ax * sin_az)
    y_rot = (x * sin_az + y * cos_az) * cos_ax - z * (cos_az * sin_ax - sin_ay * sin_az)
    z_rot = z * cos_ax * cos_ay - x * sin_ay + y * sin_ax * cos_ay
    
    return x_rot, y_rot, z_rot


def read_obj_in_chunks(filename):
    CHUNK_SIZE = 100  # Number of lines to read in a single chunk
    vertices = []
    faces = []
    
    def process_chunk(lines):
        """Process a chunk of lines from the OBJ file."""
        for line in lines:
            if line.startswith("v "):
                parts = line.split()
                vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
            elif line.startswith("f "):
                parts = line.split()
                face_indices = [int(part.split('/')[0]) - 1 for part in parts[1:]]
                for i in range(1, len(face_indices) - 1):
                    # Decompose the face into triangle fans for non-triangular faces
                    faces.append((face_indices[0], face_indices[i], face_indices[i+1]))
    
    with open(filename, 'rt') as file:
        lines = []  # Temporary list to hold lines of a chunk
        count = 0  # Counter for number of lines read so far in the current chunk
        for line in file:
            lines.append(line)
            count += 1
            if count == CHUNK_SIZE:  # If we've read CHUNK_SIZE lines, process them
                process_chunk(lines)
                lines = []  # Clear the lines list for the next chunk
                count = 0  # Reset the counter
        if lines:  # After reading the entire file, process any remaining lines
            process_chunk(lines)
    
    return vertices, faces


# Read the fox.obj file in chunks
fox_vertices, fox_faces = read_obj_in_chunks("opt_fox.obj")

def rotate_vertices(vertices, ax, ay, az):
    return [rotate_point(x, y, z, ax, ay, az) for x, y, z in vertices]

fox_vertices = rotate_vertices(fox_vertices, math.pi, 0, 0)


# Main parameters
f = 370.0  # focal length
d = 7.0  # distance from observer to projection plane
DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 240
center_x = DISPLAY_WIDTH // 2
center_y = DISPLAY_HEIGHT // 2

Y_TRANSLATION = 1.0

# Main loop
while True:
    t = time.ticks_ms() / 1000.0

    # Clear the display
    display.set_pen(WHITE)
    display.clear()

    # Rotate the object based on time
    ax, ay, az = 0, t, 0

    
    for face in fox_faces:
        if len(face) != 3:
            continue  # We only handle triangles for now

        x1, y1, z1 = rotate_point(*fox_vertices[face[0]], ax, ay, az)
        x2, y2, z2 = rotate_point(*fox_vertices[face[1]], ax, ay, az)
        x3, y3, z3 = rotate_point(*fox_vertices[face[2]], ax, ay, az)


        # Project the 3D points to 2D
        px1, py1 = project_3d_to_2d(x1, y1+Y_TRANSLATION, z1, f, d, center_x, center_y)
        px2, py2 = project_3d_to_2d(x2, y2+Y_TRANSLATION, z2, f, d, center_x, center_y)
        px3, py3 = project_3d_to_2d(x3, y3+Y_TRANSLATION, z3, f, d, center_x, center_y)

        # Compute the shading for the triangle based on the average depth
        shade = int(compute_shade((z1 + z2 + z3) / 3, -2, 2, 50, 255))
        pen = display.create_pen(shade, shade, shade)
        display.set_pen(pen)
        display.triangle(int(px1), int(py1), int(px2), int(py2), int(px3), int(py3))


    display.update()
    time.sleep(0.05)

