import pygame
#import math
from resources.grid import (make_grid, get_clicked_pos, draw, WIN, WIDTH)
#from queue import PriorityQueue, Queue
#import queue
from algoritms.bfs import breadth_first_search
from algoritms.a_star import a_star
from algoritms.dijkstras import dijkstras
from algoritms.dfs import depth_first_search
#from classes.spot import Spot


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
                    dijkstras(lambda: draw(win, grid, ROWS, width),
                              grid, start, end)

                if event.key == pygame.K_2 and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                     # Lambda is an anonymous function. This function contains a function call
                     # meaning that if the lambda function is called, it will instantly call the draw function
                    a_star(lambda: draw(win, grid, ROWS, width),
                           grid, start, end)

                if event.key == pygame.K_3 and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                     # Lambda is an anonymous function. This function contains a function call
                     # meaning that if the lambda function is called, it will instantly call the draw function
                    breadth_first_search(lambda: draw(win, grid, ROWS, width),
                                         grid, start, end)

                if event.key == pygame.K_4 and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    visited = {start}
                    nodes_in_path = [start]
                    depth_first_search(lambda: draw(win, grid, ROWS, width),
                                       grid, start, end, visited, nodes_in_path)

    pygame.quit()


if __name__ == "__main__":
    main(WIN, WIDTH)
