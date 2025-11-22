import pygame
import sys

# Налаштування
pygame.init()
WIDTH, HEIGHT = 600, 600
TILE = 40  # розмір однієї клітинки
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пакмен")

clock = pygame.time.Clock()
FPS = 60

# Лабіринт
# 0 - порожньо, 1 - стіна, 2 - точка
level = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,1,2,2,2,2,2,2,2,1,2,1],
    [1,2,1,2,1,2,1,1,1,1,1,2,1,2,1],
    [1,2,1,2,2,2,2,2,2,2,1,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,2,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,1,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,2,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

ROWS = len(level)
COLS = len(level[0])

# Кольори
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Пакмен
pacman_pos = [TILE + TILE//2, TILE + TILE//2]  # x, y в пікселях
speed = 5
direction = [0, 0]  # dx, dy

# Функції
def draw_level():
    for row in range(ROWS):
        for col in range(COLS):
            tile = level[row][col]
            x = col * TILE
            y = row * TILE
            if tile == 1:
                pygame.draw.rect(screen, BLUE, (x, y, TILE, TILE))
            elif tile == 2:
                pygame.draw.circle(screen, WHITE, (x+TILE//2, y+TILE//2), 4)

def move_pacman():
    global pacman_pos
    new_x = pacman_pos[0] + direction[0]
    new_y = pacman_pos[1] + direction[1]

    # перевірка на зіткнення зі стіною
    col = new_x // TILE
    row = new_y // TILE

    # обмеження по лабіринту
    if 0 <= row < ROWS and 0 <= col < COLS and level[row][col] != 1:
        pacman_pos[0] = new_x
        pacman_pos[1] = new_y
        # з’їдаємо точку, якщо центр пакмена потрапив на неї
        if level[row][col] == 2:
            level[row][col] = 0

def draw_pacman():
    pygame.draw.circle(screen, YELLOW, (int(pacman_pos[0]), int(pacman_pos[1])), TILE//2-2)

# Головний цикл
while True:
    screen.fill(BLACK)

    # Події
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction = [-speed, 0]
            elif event.key == pygame.K_RIGHT:
                direction = [speed, 0]
            elif event.key == pygame.K_UP:
                direction = [0, -speed]
            elif event.key == pygame.K_DOWN:
                direction = [0, speed]
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                direction = [0, 0]

    move_pacman()
    draw_level()
    draw_pacman()

    pygame.display.flip()
    clock.tick(FPS)
