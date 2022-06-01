import pygame
from classes.spot import Spot

# Set up the window
WIDTH = 700
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

# Get all the color required for the visualizer
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


# Make the grid
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

# Draw the grid lines


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        # HORIZONTAL LINES as we can see, x coordinate of start and end point is 0 and width
        # The y coordinate is the same for start and end hence horizontal
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            # VERTICAL LINES as we can see, y coordinate of start (0) and end (width)
            # The x coordinate is the same for both hence vertical line
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


# Function that will run at the start of every frame
def draw(win, grid, rows, width):
    win.fill(WHITE)
    # Draw all the squares in the grid
    for row in grid:
        for spot in row:
            spot.draw(win)
    # Draw all the lines in the grid
    draw_grid(win, rows, width)
    # Update the display
    pygame.display.update()

# Translate mouse position to know which square to change


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col
