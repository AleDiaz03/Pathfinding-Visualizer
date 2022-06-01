
import pygame
from resources.reconstruct_path import reconstruct_path


def depth_first_search(draw, grid, start, end, visited, nodes_in_path):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    if len(nodes_in_path) == 0:
        return False

    current = nodes_in_path[len(nodes_in_path) - 1]
    current.make_open()

    if current == end:
        path = {}
        for i in range(len(nodes_in_path)):
            if i != 0:
                path[nodes_in_path[i]] = nodes_in_path[i-1]
        reconstruct_path(path, current, draw)
        end.make_end()
        return True

    for neighbor in current.neighbors:
        if neighbor not in visited:
            visited.add(neighbor)
            nodes_in_path.append(neighbor)
            in_path = depth_first_search(
                draw, grid, start, end, visited, nodes_in_path)
            if in_path:
                return True
            else:
                nodes_in_path.pop()
