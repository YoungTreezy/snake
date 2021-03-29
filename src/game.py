#!usr/bin/python3
import pygame
import random

WIDTH = 540
HEIGHT = 740
FPS = 15
SIZE_BLOCK = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (224, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")
clock = pygame.time.Clock()


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # создание тела змейки
        self.image = pygame.Surface((SIZE_BLOCK, SIZE_BLOCK))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = [WIDTH/2, HEIGHT/2]
        # изначально змейка идет вправо
        self.speedx = 20
        self.speedy = 0

    def update(self):
        # изменение координат змейки
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def tail(self, size_block, snake_list):
        # рост хвоста змейки
        for x in snake_list:
            pygame.draw.rect(screen, GREEN, [x[0], x[1], size_block, size_block])

    def is_inside(self):
        # проверка находится ли змейка внутри поля
        return 0 <= self.rect.x < WIDTH and 0 <= self.rect.y < HEIGHT


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # создание яблкока
        self.image = pygame.Surface((SIZE_BLOCK, SIZE_BLOCK))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # добавление случайных координат где будет лежать яблоко
        self.foodx = round(random.randrange(0, WIDTH - SIZE_BLOCK) / 20.0) * 20.0
        self.foody = round(random.randrange(0, HEIGHT - SIZE_BLOCK) / 20.0) * 20.0

    def update(self):
        # генерация яблока в случайном месте
        self.rect.x = self.foodx
        self.rect.y = self.foody


# создание спрайтов
all_sprites = pygame.sprite.Group()
apples = pygame.sprite.Group()
snake = Snake()
all_sprites.add(snake)
apple = Apple()
all_sprites.add(apple)
apples.add(apple)


snake_list = []
len_of_snake = 1
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # проверка нажатия клавиш
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and snake.speedy != 0:
                snake.speedx = -SIZE_BLOCK
                snake.speedy = 0
            if event.key == pygame.K_d and snake.speedy != 0:
                snake.speedx = SIZE_BLOCK
                snake.speedy = 0
            if event.key == pygame.K_w and snake.speedx != 0:
                snake.speedx = 0
                snake.speedy = -SIZE_BLOCK
            if event.key == pygame.K_s and snake.speedx != 0:
                snake.speedx = 0
                snake.speedy = SIZE_BLOCK

    # конец игры если змейка вышла за поле
    if not snake.is_inside():
        running = False

    # проверка координат головы змеи
    snake_head = [snake.rect.x, snake.rect.y]
    snake_list.append(snake_head)

    # если змейка врезается в свой хвост, игра заканчивается
    for x in snake_list[:-1]:
        if x == snake_head:
            running = False

    collide = pygame.sprite.spritecollide(snake, apples, True)
    # проверка столкновения змейки с яблоком
    # если яблоко было съедено, то змейка начинает расти
    # иначе хвост удаляется
    if collide:
        snake.tail(SIZE_BLOCK, snake_list)
        apple = Apple()
        all_sprites.add(apple)
        apples.add(apple)
        len_of_snake += 1
    else: del snake_list[0]
    snake.update()
    apple.update()
    pygame.display.flip()

pygame.quit()
