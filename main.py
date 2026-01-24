import pygame
import os

# инициализация pygame
pygame.init()

# параметры окна
SCREEN_WIDTH = 2400
SCREEN_HEIGHT = 1200

# цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario Game")

# загрузка изображений
player_img = pygame.image.load(os.path.join('player.png'))
player_rect = player_img.get_rect()

# начальные координаты игрока
player_x = 50
player_y = SCREEN_HEIGHT - player_rect.height

# параметры движения игрока
player_speed = 5
player_jump = False
player_jump_speed = 10
player_jump_height = 100

# гравитация
gravity = 1

# цикл игры
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_SPACE] and not player_jump:
        player_jump = True

    if player_jump:
        player_y -= player_jump_speed
        player_jump_speed -= gravity

        if player_jump_speed < 0:
            player_jump = False
            player_jump_speed = 10

    if player_y < SCREEN_HEIGHT - player_rect.height:
        player_y += gravity

    if player_y >= SCREEN_HEIGHT - player_rect.height:
        player_y = SCREEN_HEIGHT - player_rect.height

    screen.blit(player_img, (player_x, player_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()