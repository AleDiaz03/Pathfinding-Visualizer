import pygame


def reconstruct_path(came_from, current, draw):
    while current in came_from:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = came_from[current]
        current.make_path()
        draw()
