import pygame
import numpy as np

import gol_display as D

# d(state, count) = new_state
# ---------------------------
# d(alive, 2 | 3) = alive
# d( dead,     3) = alive
# d(else)         = dead

GRID_W, GRID_H = 80, 80

GRID_INITIAL = np.random.choice(a=[0,1], size=(GRID_W * GRID_H,), p=[0.7, 0.3])
GRID_LAST_STEP = [0] * (GRID_W * GRID_H)

def wrap_toroidal(x, y):
    # assert x >= -1
    # assert x <= GRID_W
    # assert y >= -1
    # assert y <= GRID_H
    if x < 0:
        x = GRID_W - 1
    if y < 0:
        y = GRID_H - 1
    if x >= GRID_W:
        x = 0
    if y >= GRID_H:
        y = 0
    return x, y

def wrap_none(x, y):
    if x < 0 or y < 0 or x >= GRID_W or y >= GRID_H:
        return False
    return x, y

# {(u,v) : ||(x,y) - (u,v)||_\infty = 1}
def gol_neighborhood(x, y):
    return [
        (x - 1, y - 1), (x    , y - 1), (x + 1, y - 1),
        (x - 1, y    ),                 (x + 1, y    ),
        (x - 1, y + 1), (x    , y + 1), (x + 1, y + 1)
    ]

# {(u,v) : ||(x,y) - (u,v)||_1 = 1}
def one_norm_neighborhood(x, y):
    return [
                        (x    , y - 1),
        (x - 1, y    ),                 (x + 1, y    ),
                        (x    , y + 1)
    ]

# {(u,v) : ||(x,y) - (u,v)||_\infty <= r}
def gol_neighborhood_bounded(x, y, r):
    return [(x + i, y + j) for i in range(-r, r + 1) for j in range(-r, r + 1)]

def neighbors(grid, x, y, neighborhood=gol_neighborhood, wrap_func=wrap_toroidal):
    def lookup(i, j):
        r = wrap_func(i, j)
        return grid[r[1] * GRID_W + r[0]] if r else 0
    coords = neighborhood(x, y)
    count = 0
    for x, y in coords:
        count += lookup(x, y)
    return count

def neighbors_weighted(grid, x, y, r, wrap_func=wrap_none):
    def lookup(i, j):
        r = wrap_func(i, j)
        if r and r != (x, y):
            dist = max(abs(r[0] - x), abs(r[1] - y))
            return grid[r[1] * GRID_W + r[0]] / dist
        return 0
    coords = gol_neighborhood_bounded(x, y, r)
    res = 0.0
    for i, j in coords:
        res += lookup(i, j)
    return res

_STEP = 0

def step(src, dst, neighborhood=gol_neighborhood, wrap_func=wrap_none, relativize=True):
    global _STEP
    _STEP += 1
    r = 3
    r2 = 1
    k = 1
    stepped = 0
    skipped = 0
    for y in range(GRID_H):
        for x in range(GRID_W):
            index = y * GRID_W + x
            if relativize:
                w = neighbors_weighted(src, x, y, r)
            # w determines the local update speed
            if _STEP - GRID_LAST_STEP[index] > k * w * r2:
                n = neighbors(src, x, y, neighborhood=neighborhood, wrap_func=wrap_func)
                # print(w)
                s = src[index]
                if s:
                    dst[index] = (n == 2 or n == 3)
                else:
                    dst[index] = (n == 3)
                GRID_LAST_STEP[index] = _STEP
                stepped += 1
            else:
                skipped += 1
    print("stepped {} and skipped {}".format(stepped, skipped))

if __name__ == "__main__":
    screen = D.init_display()
    D.set_grid_size((GRID_W, GRID_H))

    front = GRID_INITIAL.copy()
    back = GRID_INITIAL.copy()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        step(front, back, neighborhood=gol_neighborhood)
        t = front
        front = back
        back = t
        D.render_grid(screen, front)
        pygame.display.flip()
