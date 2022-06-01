from queue import Queue
import pygame
from resources.reconstruct_path import reconstruct_path


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
