from pygame import *
from random import randint
import math
from time import time as timer


img_grass = 'grass.png'
img_zombi = 'zombi.png'
img_bullet = 'bullet.png'
img_tur = 'tur.png'
img_tur1 = 'tur1.png'

win_width = 700
win_height = 500
display.set_caption("Apocaliptoins")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_grass), (win_width, win_height))

game = True
finish = False

mixer.init()
fire_sound = mixer.Sound('fire.ogg')


font.init()
font2 = font.Font(None, 36)
font1 = font.SysFont(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
emoji_font = font.SysFont("Segoe UI Emoji", 40)

goal = 100
rel_time = False
num_fire = 0
life = 3
score = 0
lost = 0
max_lost = 10
rel_speed = 5
bullets_count = 10

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        if isinstance(player_image, str):
            self.image = transform.scale(image.load(player_image), (size_x, size_y))
        else:
            self.image = player_image  # Якщо передали Surface, а не ім'я файла
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.lvl = 1

    def update(self):
        # Отримуємо позицію миші
        mouse_x, mouse_y = mouse.get_pos()
        # Розраховуємо кут між туреллю і мишкою
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))  # обертаємо по осі Y

        # Повертаємо зображення
        self.image = transform.rotate(
            transform.scale(image.load(img_tur1), (100, 100)),
            angle
        )
        self.rect = self.image.get_rect(center=self.rect.center)  # Щоб центр не зміщувався

    def fire(self, speed):
        mouse_x, mouse_y = mouse.get_pos()
        dx = mouse_x - self.rect.centerx - 5
        dy = mouse_y - self.rect.centery - 5
        angle = math.atan2(dy, dx)

        bullet_dx = speed * math.cos(angle)
        bullet_dy = speed * math.sin(angle)

        # створюємо одразу готову повернуту картинку
        bullet_img = transform.rotate(
            transform.scale(image.load(img_bullet), (30, 10)),
            -math.degrees(angle)  # обертання треба зробити в градусах
        )

        bullet = Bullet(bullet_img, self.rect.centerx - 5, self.rect.centery - 5, 30, 10, 0)
        bullet.speed_x = bullet_dx
        bullet.speed_y = bullet_dy
        bullets.add(bullet)
        fire_sound.play()

    def lvl_up(self):
        global rel_speed, bullets_count
        self.lvl += 1
        if rel_speed > 1:
            rel_speed -= 1
        bullets_count += 3


class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y < 0 or self.rect.y > win_height or self.rect.x < 0 or self.rect.x > win_width:
            self.kill()


class Enemy(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost, life

        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            # lost = lost + 1
            life -= 1
zombis = sprite.Group()

class WaveManager:
    def __init__(self):
        self.wave_number = 1
        self.zombies_per_wave = 5
        self.zombies_remaining = self.zombies_per_wave

    def next_wave(self):
        tur1.lvl_up()
        self.wave_number += 1
        self.zombies_per_wave = 5 + self.wave_number * 2  # щораз більше зомбі
        self.zombies_remaining = self.zombies_per_wave
        self.spawn_wave()

    def spawn_wave(self):
        for _ in range(self.zombies_per_wave):
            zombi = Enemy(img_zombi, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            zombis.add(zombi)

    def zombie_killed(self):
        self.zombies_remaining -= 1
        if self.zombies_remaining <= 0:
            return True  # Хвиля завершена
        return False


wave_manager = WaveManager()
wave_manager.spawn_wave()
tur = GameSprite(img_tur, (win_width - 120)//2, win_height - 157, 120, 120, 0)
tur1 = Player(img_tur1, (win_width - 100)//2, win_height - 148, 100, 100, 0)





bullets = sprite.Group()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN and e.button == 1:


            if num_fire < bullets_count and rel_time == False:  # ⬅️
                num_fire = num_fire + 1  # ⬅️
                fire_sound.play()  # ⬅️ додали відступ
                tur1.fire(15)  # ⬅️ додали відступ

            if num_fire >= bullets_count and rel_time == False:  # якщо гравець зробив 5 пострілів⬅️
                last_time = timer()  # засікаємо час, коли це сталося⬅️
                rel_time = True  # ставимо прапор перезарядки⬅️

    if not finish:

        window.blit(background, (0, 0))

        wave_text = font2.render(f'Хвиля: {wave_manager.wave_number}', True, (255, 255, 0))
        window.blit(wave_text, (10, 10))

        tur.update()
        tur.reset()

        bullets.update()
        bullets.draw(window)

        tur1.update()
        tur1.reset()

        zombis.update()
        zombis.draw(window)

        if rel_time == True:
            now_time = timer()  # зчитуємо час

            if now_time - last_time < rel_speed:  # поки не минуло 3 секунди виводимо інформацію про перезарядку
                reload = font2.render('Перезарядка...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0  # обнулюємо лічильник куль
                rel_time = False  # скидаємо прапор перезарядки


        collides = sprite.groupcollide(zombis, bullets, True, True)
        for c in collides:
            score += 1
            if wave_manager.zombie_killed():
                wave_manager.next_wave()

        if life == 0 or lost >= max_lost:  # ⬅️⬅️
            finish = True  # програли, ставимо тло і більше не керуємо спрайтами.
            window.blit(lose, (200, 200))

        # якщо спрайт торкнувся ворога зменшує життя⬅️⬅️⬅️⬅️
        if sprite.spritecollide(tur1, zombis, False):
            sprite.spritecollide(tur1, zombis, True)
            life = life - 1
            if wave_manager.zombie_killed():
                wave_manager.next_wave()

        hearts = emoji_font.render('❤️' * life, True, (255, 100, 100))
        window.blit(hearts, (win_width - 200, win_height - 50))

        lvls = font2.render('Лвл: ' + str(tur1.lvl), 1, (0, 0, 0))
        window.blit(lvls, (80, win_height - 70))

        mon_count = font2.render('Вбито зомбі:' + str(score), 1, (11, 151, 153))
        window.blit(mon_count, (490, 10))

        # перевірка виграшу: скільки очок набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))


    display.update()
    time.delay(60)

