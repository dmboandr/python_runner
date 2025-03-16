"""
Игра Runner
"""

import pygame
import random

pygame.init()  # Запускает работу pygame
clock = pygame.time.Clock()  # специальный объект для ФПС (обновления экрана)

# Создание экрана
# Создал объект экрана размером 800х400
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")


# КЛАССЫ ДЛЯ ИГРЫ
# Sprite - это совокупность картинки и области на экране
class Snail(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, size=1, type="snail"):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.direction = 1
        self.img_list = []
        self.health = 3  # количество здоровья улитки
        for i in range(1, 3):  # 1, 2
            img = pygame.image.load(f"graphics/snail/snail{i}.png").convert_alpha()
            img = pygame.transform.rotozoom(img, 0, size)
            self.img_list.append(img)  # [img1, img2]

        self.frame = 0
        self.image = self.img_list[self.frame]
        self.speed = speed
        self.rect = self.image.get_rect(bottomright=(x, y))
        self.hit_cooldown = 1000
        self.ANIMATION_COOLDOWN = 100
        if self.type == "boss":
            self.health = 100

        # отобразить здоровье улитки на экране


    def update_animation(self):
        self.ANIMATION_COOLDOWN -= 1
        if self.ANIMATION_COOLDOWN == 0:
            self.ANIMATION_COOLDOWN = 100
            self.frame += 1

        if self.frame >= len(self.img_list):
            self.frame = 0

        self.image = self.img_list[self.frame]

    def update(self):  # апдейт выполняется 60 раз в секунду
        global difficulty, lives
        self.update_animation()
        if self.type == "snail":
            self.rect.x -= self.speed + difficulty
            if self.rect.right < 0:
                number = random.randint(8, 16)  # 800 900 1000 1100 1200... 1600
                self.rect.x = number * 100
        elif self.type == "boss":
            self.rect.x -= (self.speed + difficulty) * self.direction  # 7 * -1
            if self.rect.left < -200:
                self.direction *= -1
            elif self.rect.right > 1500:
                self.direction *= -1
            if self.rect.colliderect(player_rect) and self.hit_cooldown >= 120:
                player_rect.x -= 200 * self.direction
                self.hit_cooldown = 0
                hit_sound.play()
                lives -= 1
            # мы выполняем этот код 60 раз в секунду
            self.hit_cooldown += 1


    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.direction-1, 0), self.rect)

class Fly(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.img_list = []
        for i in range(1, 3):  # 1, 2
            img = pygame.image.load(f"graphics/Fly/Fly{i}.png").convert_alpha()
            self.img_list.append(img)  # [img1, img2]

        self.image = self.img_list[0]
        self.speed = speed
        self.direction = 1
        self.cooldown = 100
        self.rect = self.image.get_rect(midright=(x, y))

    def update(self):
        if self.rect.bottom < 200:
            self.cooldown -= 1
            self.rect.y += self.direction
            if self.cooldown == 0:
                self.direction *= -1
                self.cooldown = 100

        self.rect.x -= self.speed
        if self.rect.right < 0:
            number = random.randint(16, 30)  # 800 900 1000 1100 1200... 1600
            random_y = random.randint(1, 3)
            self.rect.x = number * 100
            self.rect.y = random_y * 50


class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"graphics/bullet.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 2)
        self.speed = speed
        self.rect = self.image.get_rect(midright=(x, y))
        self.direction = direction

    def update(self):
        global kill_count
        self.rect.x += self.speed * self.direction # движение пули с определенной скоростью
        # проверка столкнулись ли с противником
        global boss_list

        for boss in boss_list:
            if boss.rect.colliderect(self):
                if boss.health < 0:
                    boss_list = []
                self.kill()  # самоуничтожение пули
                boss.health -= 5
                print(boss.health)

        for enemy in enemy_list:
            if enemy.rect.colliderect(self):
                if enemy.rect.y < 250:  # попадание по всем летающим объектам
                    enemy.speed -= 1  # если попали, то уменьшаем их скорость  на 1
                    #enemy.rect.y -= 30  #
                    if enemy.speed == 0:  # если скорость дошла до 0, т.е. мы много попали
                        enemy.kill()  # то уничтожай объект противника
                        kill_count += 1
                else:
                    enemy.health -= 1
                    if enemy.health <= 0:
                        #enemy.rect.x = -200
                        enemy.kill()  # уничтожение из объект из памяти
                enemy.rect.x += 20  # попадание в улитку, смещение её  вправо
                self.kill()  # уничтожение пули при попадании
        # уничтожение пули, если она зашла далеко за экран
        if self.rect.left + 50 > 800:
            self.kill()  # уничтожить объект, освободить память
        return boss_list

class HealthBar:
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health, x=20, y=20):
        self.health = health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, "White", (self.x-2, self.y-2, 156, 27))  # внешняя рамка для хп
        #pygame.draw.rect(screen, "white", (self.x, self.y, 150, 20))  #
        pygame.draw.rect(screen, "Red", (self.x, self.y, 150 * ratio, 24))


# функции
def platforms(direction, speed):
    if plat_rect.right >= screen.get_width() or plat_rect.left < 0:
        direction *= -1
    plat_rect.x += speed * direction
    screen.blit(plat_surface, plat_rect)
    return direction

plat_dir = 1
# картинки
sky_surface = pygame.image.load("graphics/Sky.png").convert_alpha()
ground_surface = pygame.image.load("graphics/ground.png").convert_alpha()

# текст
font = pygame.font.Font("font/Pixeltype.ttf", 50)
text_surface = font.render("Runner", False, (64, 64, 64))
text_rect = text_surface.get_rect(center=(400, 50))

defeat_text = font.render("PRESS [SPACE] TO CONTINUE", False, (64, 64, 64))
defeat_rect = defeat_text.get_rect(center=(400, 350))


# ИГРОК
player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
# переверни на 90 градусов и увеличь размер в 2 раза
player_stand = pygame.transform.rotozoom(player_stand, 90, 3)
player_index = 0
player_anim = [player_walk_1, player_walk_2]

player_surface = player_anim[player_index]
player_rect = player_surface.get_rect(midbottom=(80, 300))  # создал rectangle игрока


# КАРТИНКИ ПРОТИВНИКОВ
# улитка
snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
# муха
fly_surface = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()

# платформы
plat_surface = pygame.Surface(size=(200, 50))
plat_surface.fill("Brown")
plat_rect = plat_surface.get_rect(midbottom=(200, 200))

# hp_player
hp_surface = pygame.Surface(size=(15, 15))
hp_surface.fill("Red")
hp_rect = hp_surface.get_rect(midbottom=(100, 100))

# звуки игры
jump_sound = pygame.mixer.Sound("audio/jump.mp3")
jump_sound.set_volume(0.10)  # 0...1       0.75  = 75% громкости
music_sound = pygame.mixer.Sound("audio/music.wav")
music_sound.set_volume(0.15)
music_sound.play(loops=-1)
hit_sound = pygame.mixer.Sound("audio/hit.wav")
hit_sound.set_volume(.8)

# ПЕРЕМЕННЫЕ ДЛЯ ИГРЫ
gravity = 0  # гравитация
moving_right = False
moving_left = False
direction = -1
alive = True
boss_fight = False
on_platform = False
dy = 1
enemy_list = []  # массив с противниками
kill_count = 0
# массивы для противников
difficulty = 1  # сложность
snails_count = 3 * difficulty
flies_count = 2 * difficulty
lives = 3


# функции для игры
def play_animation():
    global player_surface, player_index
    if player_rect.bottom < 300:
        player_surface = player_jump  # замени картинку на новую
    else:
        player_index += 0.05
        if player_index >= len(player_anim):
            player_index = 0
        player_surface = player_anim[int(player_index)]


def game_timer():
    time = int(pygame.time.get_ticks() / 1000)  # время в сек
    defeat_text = font.render(f"{time}", False, (64, 64, 64))
    defeat_rect.y = 30
    screen.blit(defeat_text, defeat_rect)
    return time


# Создаем группы для множественных объектов
snail_group = pygame.sprite.Group()  # группа для всех объектов улитки
fly_group = pygame.sprite.Group()  # группа для всех объектов мухи
fireball_group = pygame.sprite.Group()

# объекты улиток
# snail1 = Snail(700, 300, 1)  # я создал одну улитку
# snail2 = Snail(1500, 300, 2)  # я создал другую улитку
# snail_group.add(snail1)  # добавляю улиток в группу
# snail_group.add(snail2)
# enemy_list.append(snail1)  # противники-улитки добавляются в список противников
# enemy_list.append(snail2)

# объекты мух
# fly1 = Fly(3000, 100, 10)  # (img, x, y, speed)
# fly_group.add(fly1)  # добавляю мух в группу
# enemy_list.append(fly1)  # противники других типов также добавляются в список
boss_list = []
boss = Snail(1300, 300, 3, 3, "boss")
boss_list.append(boss)
snail_boss_hp = HealthBar(500, 20, boss.health, 100)

# ОСНОВНОЙ ЦИКЛ ИГРЫ
game = True
while game:
    # ПРОХОД ПО СОБЫТИЯМ
    for event in pygame.event.get():
        # ТИП СОБЫТИЯ ВЫХОД
        if event.type == pygame.QUIT:
            pygame.quit()
        # ТИП СОБЫТИЯ НАЖАТИЕ КЛАВИШИ
        if event.type == pygame.KEYDOWN:
            # КЛАВИША  ПРОБЕЛ
            if alive:
                # прыжок
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    gravity = -20
                    jump_sound.play()
                if event.key == pygame.K_d:
                    # движение игрока вправо
                    moving_right = True
                if event.key == pygame.K_a:
                    # движение игрока влево
                    moving_left = True
                if event.key == pygame.K_f:                     #player_rect.height()//2
                    fireball = Fireball(player_rect.right + 10, player_rect.y + 40, 10)
                    fireball_group.add(fireball)
            else:
                if event.key == pygame.K_SPACE:  # SPACE PRESSED
                    alive = True

        # KEYUP - отжатие клавиши (когда отпускаем палец от клавиши)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                # движение игрока вправо
                moving_right = False
            if event.key == pygame.K_a:
                # движение игрока влево
                moving_left = False

    if alive:
        # нарисуй картинки на экране
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        screen.blit(text_surface, text_rect)

        game_time = game_timer()  # 0, 1, 2 ....

        # if game_time // 10 != 0:
        #     difficulty = difficulty * (game_time // 10)  # 1 * 2
        # print(difficulty)

        # snail_rect.x -= 5  # отнимаю значение 5 от x у snail_rect
        # if snail_rect.right < 0:
        #     snail_rect.x = 800

        # гравитация
        gravity += dy
        player_rect.y += gravity

        # вызываю функцию анимации игрока
        play_animation()

        # движение игрока
        if moving_right:
            player_rect.x += 5
            direction = 1
        elif moving_left:
            player_rect.x -= 5
            direction = -1

        # имитация поверхности
        if player_rect.bottom >= 300:
            player_rect.bottom = 300

        # рисуем игрока, улитку и т.д.
        screen.blit(pygame.transform.flip(player_surface, direction-1, 0), player_rect)
        fireball_group.update()
        fireball_group.draw(screen)

        # group.draw() он ищет в классе слова image и rect

        # РАЗДЕЛ С БОССОМ ##########################################

        if boss_fight == False:

            # популяция улиток
            for _ in range(snails_count - len(snail_group)):  # 3 - 2 = 1
                snail = Snail(random.randint(700, 1200), 300, 1)
                snail_group.add(snail)  # добавляю улиток в группу
                enemy_list.append(snail)

            # популяция мух
            for _ in range(flies_count - len(fly_group)):  # 3 - 2 = 1
                fly = Fly(random.randint(1500, 3000), 100, random.randint(5, 10))
                fly_group.add(fly)  # добавляю улиток в группу
                enemy_list.append(fly)

            # проход по всем улиткам и проверка столкнулись ли мы с улиткой
            for snail in snail_group:  # прохожусь по всей группе улиток
                if player_rect.colliderect(snail.rect):  # и проверяю столкнулись ли мы
                    alive = False

            # проход по всем мухам и проверка столкнулись ли мы с мухой
            for fly in fly_group:  # прохожусь по всей группе улиток
                if player_rect.colliderect(fly.rect):  # и проверяю столкнулись ли мы
                    alive = False


            if game_time == 10 and difficulty == 1:
                #music_sound.stop()
                difficulty += 1  # difficulty = 2
            elif game_time == 20 and difficulty == 2:
                difficulty += 1  # diffuculty = 3
            elif game_time == 30 and difficulty == 2:
                difficulty += 2  # diffuculty = 3
            snail_group.update()  # вызывает метод update() у каждой улитки
            snail_group.draw(screen)  # чтобы не писать screen.blit() для каждой улитки
            fly_group.update()
            fly_group.draw(screen)

            if len(fly_group) == 0:
                fly1 = Fly(3000, 100, 10)  # (img, x, y, speed)
                fly_group.add(fly1)  # добавляю мух в группу
                enemy_list.append(fly1)  # противники других типов также добавляются в список

        else:
            difficulty = 1
            ground_surface.fill("red")
            sky_surface.fill("black")
            music_sound.stop()

            plat_speed = 2
            plat_dir = platforms(plat_dir, plat_speed)
            if player_rect.colliderect(plat_rect):
                if player_rect.bottom >= plat_rect.y-40:  # and player_rect.top > plat_rect.top-20
                    on_platform = True
                    player_rect.y += -gravity
                    gravity = 0
                    #player_rect.bottom = 120
                    player_rect.x += plat_speed * plat_dir

            if plat_rect.colliderect(player_rect.x + 5, player_rect.y, player_rect.width,  player_rect.height):
                player_rect.x -= 5 * direction

            if lives == 0:
                alive = False

            screen.blit(pygame.transform.flip(player_surface, direction - 1, 0), player_rect)
            for boss in boss_list:
                boss.update()
                boss.draw()
                snail_boss_hp.draw(boss.health)

            for i in range(lives):  # 0, 1, 2
                screen.blit(hp_surface, (20 + 25 * i, 30))

            if boss.health <= 0:
                game = False

    else:
        lives = 3
        boss.health = 100
        screen.fill("#5e81a2")
        screen.blit(player_stand, (250, 100))
        defeat_text = font.render("PRESS [SPACE] TO CONTINUE", False, (64, 64, 64))
        screen.blit(defeat_text, defeat_rect)
        player_rect.x = 50
        player_rect.y = 300
        for snail in snail_group:
            snail.rect.x = random.randint(10, 15) * 100
        for fly in fly_group:
            fly.rect.x = random.randint(10, 15) * 100

    pygame.display.update()  # обнови экран
    clock.tick(60)  # 60 ФПС

while True:
    # еще радостную музыку победы
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill("White")
    defeat_text = font.render("CONGRATULATIONS!\n"
                              "YOU COMPETE THE GAME!", False, (0, 0, 0))

    screen.blit(defeat_text, (100, 200))
    pygame.display.update()  # обнови экран
    clock.tick(60)  # 60 ФПС
