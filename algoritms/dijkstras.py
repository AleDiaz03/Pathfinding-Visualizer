from queue import PriorityQueue
import pygame
from resources.reconstruct_path import reconstruct_path


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
