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
drawing_type = 0 # 0 = none, 1 = alive, 2 = dead

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            colour = (0, 0, 0) if grid[row, col] else (255, 255, 255)
            pygame.draw.rect(screen, colour, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))

def update_grid(grid):
    new_grid = np.copy(grid)
    for row in range(ROWS):
        for col in range(COLS):
            neighbours = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue

                    neighbours += grid[(row + i) % ROWS, (col + j) % COLS]

            if grid[row, col] and (neighbours < 2 or neighbours > 3):
                new_grid[row, col] = False
            elif not grid[row, col] and neighbours == 3:
                new_grid[row, col] = True

    return new_grid

while running:
    screen.fill((200, 200, 200))
    draw_grid()
    pygame.display.flip()
    clock.tick(60 if not simulate else (30 if speedup else 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not simulate:
            if event.button == 1:
                x, y = event.pos
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if 0 <= col < COLS and 0 <= row < ROWS:
                    drawing_type = 2 if grid[row, col] else 1 # Set drawing type; 1 = alive, 2 = dead
                    grid[row, col] = not grid[row, col]

        elif event.type == pygame.MOUSEBUTTONUP and not simulate:
            if event.button == 1:
                drawing_type = 0

        elif event.type == pygame.MOUSEMOTION and not simulate:
            if drawing_type:
                x, y = event.pos
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if 0 <= col < COLS and 0 <= row < ROWS:
                    if (drawing_type == 1 and not grid[row, col]) or (drawing_type == 2 and grid[row, col]):
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