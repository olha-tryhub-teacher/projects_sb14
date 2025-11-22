from pygame import *
from random import randint

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
CELL = 20

WHITE = (255, 255, 255)

init()
screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display.set_caption("Snake_game")
clock = time.Clock()

# --- Завантаження картинок ---
snake_body_left = image.load("images/snake/snake_body_left.png")
snake_body_up = image.load("images/snake/snake_body_up.png")
snake_head_left = image.load("images/snake/snake_head_left.png")
snake_head_right = image.load("images/snake/snake_head_right.png")
snake_head_up = image.load("images/snake/snake_head_up.png")
snake_head_down = image.load("images/snake/snake_head_down.png")
snake_tail_left = image.load("images/snake/snake_tail_left.png")
snake_tail_right = image.load("images/snake/snake_tail_right.png")
snake_tail_up = image.load("images/snake/snake_tail_up.png")
snake_tail_down = image.load("images/snake/snake_tail_down.png")
apple_img = image.load("images/appel.png")
background = image.load("images/background.jpg")

# --- Звуки ---
mixer.music.load("music/music_game.wav")
mixer.music.set_volume(0.5)
mixer.music.play(-1)

lvl_up = mixer.Sound("music/lvl_up.mp3")
game_over_sound = mixer.Sound("music/game_over.flac")


# --- Базовий клас ---
class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h):
        super().__init__()
        self.image = transform.scale(img, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        screen.blit(self.image, self.rect)


# --- Яблуко ---
class Apple(GameSprite):
    def __init__(self):
        grid_x = randint(0, (WINDOW_WIDTH // CELL) - 1) * CELL
        grid_y = randint(0, (WINDOW_HEIGHT // CELL) - 1) * CELL
        super().__init__(apple_img, grid_x, grid_y, CELL, CELL)
        self.spawn()

    def spawn(self):
        grid_x = randint(0, (WINDOW_WIDTH // CELL) - 1) * CELL
        grid_y = randint(0, (WINDOW_HEIGHT // CELL) - 1) * CELL
        self.rect.x = grid_x
        self.rect.y = grid_y



# --- Змійка ---
class Snake:
    def __init__(self):
        self.body = [(200, 200), (180, 200), (160, 200)]  # координати частин
        self.direction = "RIGHT"
        self.new_direction = "RIGHT"

    def update_direction(self):
        keys = key.get_pressed()

        if keys[K_UP] and self.direction != "DOWN":
            self.new_direction = "UP"
        if keys[K_DOWN] and self.direction != "UP":
            self.new_direction = "DOWN"
        if keys[K_LEFT] and self.direction != "RIGHT":
            self.new_direction = "LEFT"
        if keys[K_RIGHT] and self.direction != "LEFT":
            self.new_direction = "RIGHT"

        self.direction = self.new_direction

    def move(self):
        x, y = self.body[0]

        if self.direction == "UP":
            y -= CELL
        elif self.direction == "DOWN":
            y += CELL
        elif self.direction == "LEFT":
            x -= CELL
        elif self.direction == "RIGHT":
            x += CELL

        new_head = (x, y)

        # Додаємо нову голову
        self.body.insert(0, new_head)
        # Відрізаємо хвіст (якщо не з'їли)
        self.body.pop()

    def grow(self):
        # Додається ще одна частина — повторення хвоста
        self.body.append(self.body[-1])

    def draw(self):
        # Малюємо голову
        hx, hy = self.body[0]
        if self.direction == "LEFT":
            head_img = snake_head_left
            tail_img = snake_tail_left
        elif self.direction == "RIGHT":
            head_img = snake_head_right
            tail_img = snake_tail_right
        elif self.direction == "UP":
            head_img = snake_head_up
            tail_img = snake_tail_up
        else:
            head_img = snake_head_down
            tail_img = snake_tail_down

        screen.blit(transform.scale(head_img, (CELL, CELL)), (hx, hy))

        # Малюємо тіло
        for x, y in self.body[1:-1]:
            screen.blit(transform.scale(snake_body_left, (CELL, CELL)), (x, y))

        # Малюємо хвіст
        tx, ty = self.body[-1]
        screen.blit(transform.scale(tail_img, (CELL, CELL)), (tx, ty))

    def collide_with_walls(self):
        x, y = self.body[0]
        return not (0 <= x < WINDOW_WIDTH and 0 <= y < WINDOW_HEIGHT)

    def collide_with_self(self):
        return self.body[0] in self.body[1:]


# --- Створення об'єктів ---
snake = Snake()
apple = Apple()

running = True
while running:
    screen.blit(background, (0, 0))

    for e in event.get():
        if e.type == QUIT:
            running = False

    snake.update_direction()
    snake.move()

    # Перевірка зіткнення з яблуком
    if snake.body[0] == (apple.rect.x, apple.rect.y):
        snake.grow()
        lvl_up.play()
        apple.spawn()

    # Смерть
    if snake.collide_with_walls() or snake.collide_with_self():
        game_over_sound.play()
        running = False

    apple.draw()
    snake.draw()

    display.flip()
    clock.tick(5)  # швидкість гри
