from queue import PriorityQueue
import pygame
from resources.heuristic import h
from resources.reconstruct_path import reconstruct_path


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
