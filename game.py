import pygame
import numpy as np

# Get screen info
pygame.init()
screen_info = pygame.display.Info()
screen_height = screen_info.current_h
print(screen_height)

# Config
SCREEN_PERCENTAGE = 0.9
HEIGHT = int(screen_height * SCREEN_PERCENTAGE)
WIDTH = HEIGHT
ROWS, COLS = 50, 50
CELL_SIZE = WIDTH // COLS

# Recalculate width and height
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

# Initialize display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

grid = np.zeros((ROWS, COLS), dtype=bool)

running = True
simulate = False
speedup = False

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            colour = (0, 0, 0) if grid[row, col] else (255, 255, 255)
            pygame.draw.rect(screen, colour, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))

def update_grid(grid):
    new_grid = np.copy(grid)
    for row in range(ROWS):
        for col in range(COLS):
            neighbours = np.sum(grid[max(row-1, 0):min(row+2, ROWS), max(col-1, 0):min(col+2, COLS)]) - grid[row, col]

            if grid[row, col] and (neighbours < 2 or neighbours > 3):
                new_grid[row, col] = False
            elif not grid[row, col] and neighbours == 3:
                new_grid[row, col] = True

    return new_grid

while running:
    screen.fill((200, 200, 200))
    draw_grid()
    pygame.display.flip()
    clock.tick(30 if speedup else 10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not simulate:
            x, y = event.pos
            col = x // CELL_SIZE
            row = y // CELL_SIZE
            if 0 <= col < COLS and 0 <= row < ROWS:
                grid[row, col] = not grid[row, col]

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                simulate = not simulate
            elif event.key == pygame.K_r:
                grid = np.zeros((ROWS, COLS), dtype=bool)
                simulate = False
            elif event.key == pygame.K_LSHIFT:
                speedup = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                speedup = False

    if simulate:
        grid = update_grid(grid)

pygame.quit()