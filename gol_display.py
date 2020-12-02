import pygame

SCREEN_SIZE = (800, 800)
COLOR_ALIVE = (255, 255, 255)
COLOR_DEAD = (100, 0, 10)

_GRID_SIZE = None
_CELL_W = None
_CELL_H = None

def init_display():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("gol")
    screen.fill(COLOR_DEAD)
    return screen

def set_grid_size(size):
    global _GRID_SIZE, _CELL_W, _CELL_H
    _GRID_SIZE = size
    _CELL_W = SCREEN_SIZE[0] / size[0]
    _CELL_H = SCREEN_SIZE[1] / size[1]

def render_grid(screen, grid):
    assert _GRID_SIZE is not None
    # TODO: parallel
    for y in range(_GRID_SIZE[1]):
        for x in range(_GRID_SIZE[0]):
            alive = grid[y * _GRID_SIZE[0] + x]
            screen_x = x * _CELL_W
            screen_y = y * _CELL_H
            r = pygame.Rect(screen_x, screen_y, _CELL_W, _CELL_H)
            screen.fill(COLOR_ALIVE if alive else COLOR_DEAD, rect=r)
