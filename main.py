"""
Pygame - это модуль, который предоставляет большой
набор разных функция для управления изображениями
и расчета координат.

Для установки pygame нужно прописать в терминале

pip install pygame

Но в зависимости от настроек Pycharm и Python,
может возникнуть ситуация, что команда pip не определена
в терминале.

Если pip не распознается в терминале, но команду нужно
выполнять через python

python -m pip install pygame
"""

import pygame

pygame.init()  # Запускает работу pygame
clock = pygame.time.Clock()  # специальный объект для ФПС (обновления экрана)

# Создание экрана
# Создал объект экрана размером 800х400
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Игра")

# Создаем поверхности
#                            ширина высота
white_part = pygame.Surface((500, 100)) # создаю поверхность на координате 100, 200
white_part.fill("White")  # закрась поверхность полностью красным

blue_part = pygame.Surface((500, 100)) # создаю поверхность на координате 100, 200
blue_part.fill("Blue")  # закрась поверхность полностью красным

red_part = pygame.Surface((500, 100)) # создаю поверхность на координате 100, 200
red_part.fill("Red")  # закрась поверхность полностью красным
x = 50
y = 0
direction_x = 1
direction_y = 1


while True:
    # Проход по всем событиям
    for event in pygame.event.get():
        # перебираем разные типы событий
        if event.type == pygame.QUIT:
            pygame.quit()  # если мы нажимаем на крестик (закрыть), то закрывай программу

    screen.fill("black")
    screen.blit(white_part, (x, y + 0))  # x, y
    screen.blit(blue_part, (x, y + 100))
    screen.blit(red_part, (x, y + 200))
    x += 1 * direction_x
    y += 1 * direction_y

    if x > 300:
        direction_x *= -1
    elif x <= 0:
        direction_x *= -1

    if y > 100:
        direction_y *= -1
    elif y <= 0:
        direction_y *= -1


    pygame.display.update()  # обнови экран
    clock.tick(60)  # 60 ФПС (60 раз в секунду обновляй экран)


