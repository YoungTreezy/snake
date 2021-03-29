#!usr/bin/python3
import pygame
import random

WIDTH = 540
HEIGHT = 740
FPS = 2
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
        self.image = pygame.Surface((SIZE_BLOCK, SIZE_BLOCK))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = [WIDTH/2, HEIGHT/2]
        self.speedx = 20
        self.speedy = 0

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def tail(self, size_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(screen, GREEN, [x[0], x[1], size_block, size_block])


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((SIZE_BLOCK, SIZE_BLOCK))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.foodx = round(random.randrange(0, WIDTH - SIZE_BLOCK) / 20.0) * 20.0
        self.foody = round(random.randrange(0, HEIGHT - SIZE_BLOCK) / 20.0) * 20.0

    def update(self):
        self.rect.x = self.foodx
        self.rect.y = self.foody


all_sprites = pygame.sprite.Group()
apples = pygame.sprite.Group()
apple = Apple()
snake = Snake()
all_sprites.add(snake)
all_sprites.add(apple)
apples.add(apple)


snake_list = []
len_of_snake = 1
running = True
while running:
    clock.tick(FPS)
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

    screen.fill(BLACK)
    all_sprites.draw(screen)
    if snake.rect.left < -10:
        running = False
    if snake.rect.right > WIDTH + 10:
        running = False
    if snake.rect.top <= -10:
        running = False
    if snake.rect.bottom > HEIGHT + 10:
        running = False

    snake_head = [snake.rect.x, snake.rect.y]
    snake_list.append(snake_head)
    if len(snake_list) > len_of_snake:
        del snake_list[0]

    for x in snake_list[:-1]:
        if x == snake_head:
            running = False

    collide = pygame.sprite.spritecollide(snake, apples, True)
    if collide:
        snake.tail(SIZE_BLOCK, snake_list)
        apple = Apple()
        all_sprites.add(apple)
        apples.add(apple)
        len_of_snake += 1
        pygame.display.update()

    pygame.display.flip()
    snake.update()
    apple.update()

pygame.quit()
