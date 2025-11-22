import pygame

# кольори
YELLOW = (200, 200, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# налаштування Pygame
pygame.init()
screen = pygame.display.set_mode((500, 500))

# ваш код
img_player = pygame.image.load("DinoRun1.png").convert_alpha()
img_player2 = pygame.image.load("DinoRun2.png").convert_alpha()
img_player_jump = pygame.image.load("DinoJump.png").convert_alpha()

img_cactus = pygame.image.load("SmallCactus1.png")
img_cloud = pygame.image.load("Cloud.png")
img_ground = pygame.image.load("Track.png")


class Object:
    def __init__(self, x, y, img):
        self.img = img
        self.rect = pygame.Rect(x, y, self.img.get_width(), self.img.get_htight())

    def draw(self, screen):
        screen.bilt(self.img, (self.rect.left, self.rect.top))


# клас гравця з керуванням
class Player(Object):
    def __init__(self, x, y):
        super().__init__(x, y, img_player)
        self.max_y = y
        self.velocity = 0
        self.GRAVITY = 0.007
        self.in_air = False

    # реалізація керування і гравітації
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.in_air:
            self.velocity = 15
            self.in_air = True

        if self.in_air:
            self.rect.top -= self.velocity
            self.velocity -= self.GRAVITY
            if self.rect.top >= self.max_y:
                self.in_air = False
                self.rect.top = self.max_y

# БАЖАНО ЦЕ НАПИСАТИ ВГОРІ, ОДРАЗУ ПІСЛЯ ІМПОРТІВ
from random import randint
SPEED = 5

class MovingObject(Object):
    def update(self):
        self.rect.left -= SPEED
        if self.rect.right < 0:
            self.rect.x = randint(600, 1000)

# кактус, що рухаються ліворуч
class Cactus(MovingObject):
    def __init__(self):
        x = randint(600, 1000)
        super().__init__(x, 400, img_cactus)


# хмара
class Cloud(MovingObject):
    def __init__(self):
        x = randint(500, 1000)
        y = randint(80, 200)
        super().__init__(x, y, img_cloud)

    def update(self):
        if self.rect.right <= 0:
            self.rect.y = randint(50, 300)
        super().update()

