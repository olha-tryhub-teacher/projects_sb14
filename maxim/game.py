from pygame import *
from random import randint
win_width = 900
win_height = 700
wall_size = 50
window = display.set_mode((win_width, win_height + 100))
display.set_caption("гра у квача")
bg = transform.scale(image.load("pole.jpg"), (win_width, win_height))

x1 = 100
y1 = 70

x2 = win_width - 200
y2 = win_height - 150

tank1_hp = 2500
tank2_hp = 2700

win_flag = False

hp_line_width = win_width//3
hp_line_height = 15

GREEN = (124, 252, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)

font.init()
font_tanks = font.Font(None, 36)
T_64_hp_text = font_tanks.render("T-64", True, (255, 255, 255))
FV4202_hp_text = font_tanks.render("FV4202", True, (255, 255, 255))
T_64_win = font_tanks.render("T-64 переміг!", True, (255, 255, 255))
FV4202_win = font_tanks.render("FV4202 переміг!", True, (255, 255, 255))


grey_hp_line_1 = Rect(10, win_height + 50, hp_line_width, 15)
grey_hp_line_2 = Rect(win_width - hp_line_width - 10, win_height + 50, hp_line_width, 15)
T_64_hp_line = Rect(10, win_height + 50, hp_line_width, 15)
FV4202_hp_line = Rect(win_width - hp_line_width - 10, win_height + 50, hp_line_width, 15)



mixer.init()
mixer.music.load("War_Thunder.mp3")
mixer.music.play(-1)
T_64_fire_sound = mixer.Sound("postril-1.mp3")
FV4202_fire_sound = mixer.Sound("postril-2.mp3")
win_sound = mixer.Sound("win.mp3")


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed, direction=""):
        super().__init__()
        if not direction:
            self.image = transform.scale(image.load(player_image), (width, height))
        else:
            if direction == "left":
                self.image = transform.rotate(transform.scale(image.load(player_image), (width, height)), 90)
            elif direction == "right":
                self.image = transform.rotate(transform.scale(image.load(player_image), (width, height)), -90)
            if direction == "up":
                self.image = transform.rotate(transform.scale(image.load(player_image), (width, height)), 0)
            elif direction == "down":
                self.image = transform.rotate(transform.scale(image.load(player_image), (width, height)), 180)
        self.image_path = player_image
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.width = width
        self.height = height
        self.direction = direction

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class SpriteRectWrapper(sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect


# нові класи-спадкоємці
class Tank(GameSprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed, direction, hp, damage):
        super().__init__(player_image, player_x, player_y, width, height, player_speed)
        self.direction = direction
        self.hp = hp
        self.damage = damage

        # Менший rect для колізій (тіло танка без дула)
        self.hitbox_width = int(width)
        self.hitbox_height = int(width)
        self.hitbox = Rect(0, 0, self.hitbox_width, self.hitbox_height)

        self.hitbox.center = self.rect.center

    def update(self, key_up, key_down, key_left, key_right, walls_groups):
        keys = key.get_pressed()

        dx = 0
        dy = 0
        rotated = False

        if keys[key_left]:
            dx = -self.speed
            new_image = transform.rotate(transform.scale(image.load(self.image_path), (self.width, self.height)), 90)
            if self.direction != "left" or self.direction != "right":
                center_x = self.hitbox.centerx
                center_y = self.hitbox.centery
                self.hitbox = Rect(self.hitbox.x, self.hitbox.y, self.hitbox_height, self.hitbox_width)
                self.hitbox.centerx, self.hitbox.centery = center_x, center_y
            self.direction = "left"
            rotated = True
        elif keys[key_right]:
            dx = self.speed
            new_image = transform.rotate(transform.scale(image.load(self.image_path), (self.width, self.height)), -90)
            if self.direction != "left" or self.direction != "right":
                center_x = self.hitbox.centerx
                center_y = self.hitbox.centery
                self.hitbox = Rect(self.hitbox.x, self.hitbox.y, self.hitbox_height, self.hitbox_width)
                self.hitbox.centerx, self.hitbox.centery = center_x, center_y
            self.direction = "right"
            rotated = True
        elif keys[key_up]:
            dy = -self.speed
            new_image = transform.scale(image.load(self.image_path), (self.width, self.height))
            if self.direction != "up" or self.direction != "down":
                center_x = self.hitbox.centerx
                center_y = self.hitbox.centery
                self.hitbox = Rect(self.hitbox.x, self.hitbox.y, self.hitbox_width, self.hitbox_height)
                self.hitbox.centerx, self.hitbox.centery = center_x, center_y
            self.direction = "up"
            rotated = True
        elif keys[key_down]:
            dy = self.speed
            new_image = transform.rotate(transform.scale(image.load(self.image_path), (self.width, self.height)), 180)
            if self.direction != "up" or self.direction != "down":
                center_x = self.hitbox.centerx
                center_y = self.hitbox.centery
                self.hitbox = Rect(self.hitbox.x, self.hitbox.y, self.hitbox_width, self.hitbox_height)
                self.hitbox.centerx, self.hitbox.centery = center_x, center_y
            self.direction = "down"
            rotated = True
        else:
            new_image = self.image

        # === Перевірка колізій по X ===
        future_hitbox_x = self.hitbox.move(dx, 0)
        collision_x = False
        for wall_group in walls_groups:
            if sprite.spritecollideany(SpriteRectWrapper(future_hitbox_x), wall_group):
                collision_x = True
                break
        if not collision_x:
            self.hitbox.x += dx

        # === Перевірка колізій по Y ===
        future_hitbox_y = self.hitbox.move(0, dy)
        collision_y = False
        for wall_group in walls_groups:
            if sprite.spritecollideany(SpriteRectWrapper(future_hitbox_y), wall_group):
                collision_y = True
                break
        if not collision_y:
            self.hitbox.y += dy

        # === Позиція картинки має відповідати hitbox.center ===
        self.rect.center = self.hitbox.center

        # === Оновлюємо картинку після повороту ===
        if rotated:
            self.image = new_image
            self.rect = self.image.get_rect(center=self.hitbox.center)

    def fire(self, fire_sound):
        fire_sound.play()
        if self.direction in ["up", "down"]:
            shell = Shell("snaryad.png", self.rect.centerx, self.rect.centery, 15, 20, 15, self.direction, self)
        else:
            shell = Shell("snaryad.png", self.rect.centerx, self.rect.centery, 20, 15, 15, self.direction, self)
        shells.add(shell)


class Wall(GameSprite):
    def __init__(self, wall_img, player_x, player_y):
        super().__init__(wall_img, player_x, player_y, wall_size, wall_size, 0)


class StoneWall(Wall):
    def __init__(self, player_x, player_y):
        super().__init__("stone-wall.jpg", player_x, player_y)


class BrickWall(Wall):
    def __init__(self, player_x, player_y):
        super().__init__("brick-wall.png", player_x, player_y)


class Shell(GameSprite):
    def __init__(self, player_image, player_x, player_y, width, height, speed, direction, owner):
        super().__init__(player_image, player_x, player_y, width, height, speed)
        self.direction = direction
        self.owner = owner  # власник снаряда (tank1 або tank2)

    def update(self):
        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed



tank1 = Tank("T64_5.gif", x1, y1, 50, 120, 5, "left", tank1_hp, 350)
tank2 = Tank("tank2.png", x2, y2, 50, 120, 5, "right", tank2_hp, 380)
ring_prize = GameSprite("winner.png", (win_width-120)//2, (win_height-120)//2, 80, 73, 0)

shells = sprite.Group()

# код для створення стінок
# створення рамки
stone_walls = sprite.Group()
width_stone_walls = win_width // wall_size
height_stone_walls = win_height // wall_size

x = 0
y = 0
for i in range(width_stone_walls):
    stone_wall = StoneWall(x, y)
    stone_walls.add(stone_wall)
    x += wall_size

x = 0
y = win_height - wall_size
for i in range(width_stone_walls):
    stone_wall = StoneWall(x, y)
    stone_walls.add(stone_wall)
    x += wall_size

x = 0
y = 0
for i in range(height_stone_walls):
    stone_wall = StoneWall(x, y)
    stone_walls.add(stone_wall)
    y += wall_size

x = win_width - wall_size
y = 0
for i in range(height_stone_walls):
    stone_wall = StoneWall(x, y)
    stone_walls.add(stone_wall)
    y += wall_size

# створення рандомних кам'яних стін перешкод
stone_wall = StoneWall(wall_size * 1, wall_size*4)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 2, wall_size*4)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 3, wall_size*4)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 7, wall_size*1)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 8, wall_size*1)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 7, wall_size*2)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 6, wall_size*4)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 7, wall_size*4)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 8, wall_size*4)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 9, wall_size*4)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 10, wall_size*4)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 11, wall_size*4)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 12, wall_size*4)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 13, wall_size*4)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 14, wall_size*4)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 10, wall_size*3)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 11, wall_size*3)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 14, wall_size*3)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 10, wall_size*8)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 9, wall_size*8)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 8, wall_size*8)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 7, wall_size*8)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 6, wall_size*8)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 5, wall_size*6)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 4, wall_size*6)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 3, wall_size*6)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 1, wall_size*10)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 2, wall_size*10)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 3, wall_size*10)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 10, wall_size*10)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 10, wall_size*11)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 11, wall_size*11)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 9, wall_size*11)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 8, wall_size*11)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 8, wall_size*12)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 7, wall_size*12)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 6, wall_size*12)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 5, wall_size*12)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 7, wall_size*10)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 7, wall_size*11)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 9, wall_size*12)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 13, wall_size*9)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 14, wall_size*9)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 15, wall_size*9)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 13, wall_size*8)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 14, wall_size*8)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 15, wall_size*8)
stone_walls.add(stone_wall)
stone_wall = StoneWall(wall_size * 13, wall_size*7)
stone_walls.add(stone_wall)

# створення цегляних перешкод
brick_walls = sprite.Group()
brick_wall = BrickWall(wall_size * 4, wall_size * 4)
brick_walls.add(brick_wall)
brick_wall = BrickWall(wall_size * 5, wall_size * 4)
brick_walls.add(brick_wall)
brick_wall = BrickWall(wall_size * 14, wall_size * 2)
brick_walls.add(brick_wall)
brick_wall = BrickWall(wall_size * 14, wall_size * 5)
brick_walls.add(brick_wall)
brick_wall = BrickWall(wall_size * 13, wall_size * 5)
brick_walls.add(brick_wall)
brick_wall = BrickWall(wall_size * 15, wall_size * 5)
brick_walls.add(brick_wall)
brick_wall = BrickWall(wall_size * 13, wall_size * 6)
brick_walls.add(brick_wall)
brick_wall = BrickWall(wall_size * 12, wall_size * 8)
brick_walls.add(brick_wall)
brick_wall = BrickWall(wall_size * 11, wall_size * 8)
brick_walls.add(brick_wall)
brick_wall = BrickWall(wall_size * 10, wall_size * 7)
brick_walls.add(brick_wall)
brick_wall = BrickWall(wall_size * 10, wall_size * 6)
brick_walls.add(brick_wall)
brick_wall = BrickWall(wall_size * 10, wall_size * 5)
brick_walls.add(brick_wall)
brick_wall = BrickWall(wall_size * 6, wall_size * 5)
brick_walls.add(brick_wall)
brick_wall = BrickWall(wall_size * 6,wall_size * 6)
brick_walls.add(brick_wall)
brick_wall = BrickWall(wall_size * 6,wall_size * 7)
brick_walls.add(brick_wall)
brick_wall = BrickWall(wall_size * 5,wall_size * 9)
brick_walls.add(brick_wall)
brick_wall = BrickWall(wall_size * 4,wall_size * 9)
brick_walls.add(brick_wall)
brick_wall = BrickWall(wall_size * 5,wall_size * 10)
brick_walls.add(brick_wall)
brick_wall = BrickWall(wall_size * 5,wall_size * 11)
brick_walls.add(brick_wall)
brick_wall = BrickWall(wall_size * 3,wall_size * 9)
brick_walls.add(brick_wall)

walls_groups = [stone_walls, brick_walls]
run = True
clock = time.Clock()
FPS = 60
speed = 5

while run:
    window.blit(bg, (0, 0))

    if tank1.hp <= 0 or tank2.hp <= 0:
        ring_prize.reset()
        if ring_prize.rect.colliderect(tank1.rect):
            window.blit(T_64_win, (win_width // 2 - 100, win_height + 10))
            if not win_flag:
                win_sound.play()
                win_flag = True
        if ring_prize.rect.colliderect(tank2.rect):
            window.blit(FV4202_win, (win_width // 2 - 100, win_height + 10))
            if not win_flag:
                win_sound.play()
                win_flag = True

    if tank1.hp > 0:
        tank1.reset()
        tank1.update(K_w, K_s, K_a, K_d, walls_groups)

    if tank2.hp > 0:
        tank2.reset()
        tank2.update(K_UP, K_DOWN, K_LEFT, K_RIGHT, walls_groups)

    stone_walls.draw(window)
    brick_walls.draw(window)

    shells.draw(window)
    shells.update()

    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                tank2.fire(T_64_fire_sound)
            elif e.key == K_e:
                tank1.fire(FV4202_fire_sound)

    # Снаряд знищує brick walls
    collides_brick = sprite.groupcollide(shells, brick_walls, True, True)

    # Снаряд стикається зі stone walls, але стіна не зникає
    collides_stone = sprite.groupcollide(shells, stone_walls, True, False)

    # Копія списку, бо будемо видаляти елементи
    for shell in shells.copy():
        # Влучання в tank1, якщо стріляв не tank1
        if shell.owner != tank1 and shell.rect.colliderect(tank1.rect):
            tank1.hp -= shell.owner.damage
            shells.remove(shell)

        # Влучання в tank2, якщо стріляв не tank2
        elif shell.owner != tank2 and shell.rect.colliderect(tank2.rect):
            tank2.hp -= shell.owner.damage
            shells.remove(shell)

    window.blit(T_64_hp_text, (10, win_height + 10))
    window.blit(FV4202_hp_text, (win_width - 100, win_height + 10))

    draw.rect(window, GREY, grey_hp_line_1)
    draw.rect(window, GREY, grey_hp_line_2)

    if tank1.hp > 0:
        T_64_hp_line.width = tank1.hp / tank1_hp * hp_line_width
    else:
        T_64_hp_line.width = 0

    if tank2.hp > 0:
        FV4202_hp_line.width = tank2.hp / tank2_hp * hp_line_width
    else:
        FV4202_hp_line.width = 0

    if tank1.hp >= tank1_hp / 2:
        draw.rect(window, GREEN, T_64_hp_line)
    elif tank1.hp >= tank1_hp / 4:
        draw.rect(window, ORANGE, T_64_hp_line)
    else:
        draw.rect(window, RED, T_64_hp_line)

    if tank2.hp >= tank2_hp / 2:
        draw.rect(window, GREEN, FV4202_hp_line)
    elif tank2.hp >= tank2_hp / 4:
        draw.rect(window, ORANGE, FV4202_hp_line)
    else:
        draw.rect(window, RED, FV4202_hp_line)


    display.update()
    clock.tick(FPS)
