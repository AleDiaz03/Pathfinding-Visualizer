import pygame
import math
from queue import PriorityQueue, Queue
import queue

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

# Create class for node (each square in grid)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        # Check north east south west and if not barrier add to neighbor list
        self.neighbors = []
        # Check SOUTH
        # First part of if checks that if we are in the last row to avoid index error
        # Second part checks if south neighbor is a barrier or not
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Check NORTH
        # Check if top row
        # Check if node above is barrier
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        # Check EAST
        # Check if last col
        # Chech if col to the right is a barrier
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Check WEST
        # Check if first column
        # Check if node to the left is a barrier
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    # We are defining the less than operator so we can compare Nodes
    def __lt__(self, other):
        return False

# Heuristic Value


def h(p1, p2):
    # We are using Manhattan distance to calculate heuristic
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# Function to reconstruct the path


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

# ALGORITHM FUNCTION


def breadth_first_search(draw, grid, start, end):
    open_set = Queue()
    open_set.put(start)
    closed_set = {start}
    came_from = {}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        for neighbor in current.neighbors:
            if neighbor not in closed_set:
                open_set.put(neighbor)
                closed_set.add(neighbor)
                came_from[neighbor] = current
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False


def dijkstras(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    closed_set = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[1]
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                if neighbor not in closed_set:
                    count += 1
                    open_set.put((count, neighbor))
                    closed_set.add(neighbor)
                    neighbor.make_open()
        draw()
        if current != start:
            current.make_closed()

    return False


def a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    # Start the algorithm by adding the start node into the open list
    # Set the f-score of the start to 0
    # Count will be used for tie brakers
    open_set.put((0, count, start))
    # Create a map that shows predecessors for all nodes, so we can construct the path
    came_from = {}
    # Create map to store the g_score of all nodes
    # All nodes start with a g_score of infinity
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    # Create a map to store f_score of all nodes
    f_score = {spot: float("inf") for row in grid for spot in row}
    # As g score of start is 0 the f score is just the h score f = g + h, g = 0 so f = h
    f_score[start] = h(start.get_pos(), end.get_pos())
    # Create a closed list that stores all the nodes that are in the priority queue or have been visited\
    # This is a set
    closed_set = {start}

    # Algorithm runs while open set is not empty
    # If empty that means there is no solution
    while not open_set.empty():
        # Again, allow user to quit program if desired
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        # Pop the node from the priority queue
        # The [2] means it is popping the node so fscore [0], count [1], node[2]
        current = open_set.get()[2]

        # If we are looking at the end node, we found a path
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            # The g score of the neighbor is the g score of the current plus one
            temp_g_score = g_score[current] + 1

            # If this calculated g score is smaller than the current gscore for the neighbor
            # Update the gscore of the neighbor
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + \
                    h(neighbor.get_pos(), end.get_pos())
                # Check if neighbor is in closed list, if it is then ignore neighbor
                # Else then add it to both the open and closed list and change color with makeopen
                if neighbor not in closed_set:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    closed_set.add(neighbor)
                    neighbor.make_open()

        # Update the screen
        draw()

        # After we look at a node, change color to signal it is closed
        # If it is the start however, color should not change hence the if statement
        if current != start:
            current.make_closed()

    return False

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


def main(win, width):
    # Define the number of rows. Making this a variable at the beginning means that
    # just by changing this value we will be able to modify the amount of squares in the grid
    ROWS = 50
    grid = make_grid(ROWS, width)
    # The start and end squares of the path, at start they are null and user has to set them
    start = None
    end = None
    # Keep track of state of the program
    run = True
    while run:
        draw(win, grid, ROWS, width)
        # Loop through all pygame events e.g mouse click, key press...
        for event in pygame.event.get():
            # If user clicks the x button at the top right, then quit the game
            if event.type == pygame.QUIT:
                run = False

            # Check for a LEFT mouse click
            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                # Check if the start position has been selected
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()
            # Check for a RIGHT mouse click
            # 1 is for the middle mouse click
            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                # When right click pressed, we are undoing or resetting the node
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                # Handle case where undoing start or end
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                     # Lambda is an anonymous function. This function contains a function call
                     # meaning that if the lambda function is called, it will instantly call the draw function
                    dijkstras(lambda: draw(win, grid, ROWS, width),
                              grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_1 and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                     # Lambda is an anonymous function. This function contains a function call
                     # meaning that if the lambda function is called, it will instantly call the draw function
                    a_star(lambda: draw(win, grid, ROWS, width),
                           grid, start, end)

                if event.key == pygame.K_2 and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                     # Lambda is an anonymous function. This function contains a function call
                     # meaning that if the lambda function is called, it will instantly call the draw function
                    breadth_first_search(lambda: draw(win, grid, ROWS, width),
                                         grid, start, end)

    pygame.quit()


if __name__ == "__main__":
    main(WIN, WIDTH)