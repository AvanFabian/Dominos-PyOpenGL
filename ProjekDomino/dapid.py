import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Domino")

# OpenGL initialization
glOrtho(0, width, 0, height, -1, 1)

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define the square game board
board_size = 400
board_left = (width - board_size) // 2
board_bottom = (height - board_size) // 2

# Calculate the positions of 8 dots in the shape of a circle
num_dots = 8
circle_center = (board_left + board_size // 2, board_bottom + board_size // 2)
circle_radius = board_size // 2

# Calculate the positions of 8 dots in a circular arrangement
dot_positions = []
for i in range(num_dots):
    angle = i * (360 / num_dots)
    x = int(circle_center[0] + circle_radius * math.cos(math.radians(angle)))
    y = int(circle_center[1] + circle_radius * math.sin(math.radians(angle)))
    dot_positions.append((x, y))

# OpenGL draw function
def draw():
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw the square game board
    glBegin(GL_LINE_LOOP)
    glColor3fv(RED)
    glVertex2f(board_left, board_bottom)
    glVertex2f(board_left + board_size, board_bottom)
    glVertex2f(board_left + board_size, board_bottom + board_size)
    glVertex2f(board_left, board_bottom + board_size)
    glEnd()

    # Draw the dots in the shape of a circle
    glPointSize(10.0)
    glBegin(GL_POINTS)
    for dot in dot_positions:
        glVertex2fv(dot)
    glEnd()

    # Draw lines connecting each point to the next one
    glBegin(GL_LINES)
    for i in range(num_dots):
        glVertex2fv(dot_positions[i])
        glVertex2fv(dot_positions[(i + 2) % num_dots])
    glEnd()

    pygame.display.flip()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    draw()
    pygame.time.wait(10)