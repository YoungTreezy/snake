#!usr/bin/python3
import pygame
import random
import pygame_menu

pygame.init()
WIDTH = 540
HEIGHT = 740
bg_img = pygame.image.load('img/snake.jpg')
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def start_the_game():
    FPS = 3
    SIZE_BLOCK = 20

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (224, 0, 0)
    TAIL_COLOR = (0, 255, 0)
    BLUE = (0, 0, 255)
    HEADER_COLOR = (0, 204, 153)
    FRAME_COLOR = (0, 255, 204)
    SNAKE_COLOR = (0, 102, 0)

    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    courier = pygame.font.SysFont('courier', 36)

    class Snake(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            # создание тела змейки
            self.image = pygame.Surface((SIZE_BLOCK, SIZE_BLOCK))
            self.image.fill(SNAKE_COLOR)
            self.rect = self.image.get_rect()
            self.rect.center = [WIDTH / 2, HEIGHT / 2]
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
                pygame.draw.rect(screen, SNAKE_COLOR, [x[0], x[1], size_block, size_block])

        def is_inside(self):
            # проверка находится ли змейка внутри поля
            return 0 <= self.rect.x < WIDTH and 200 <= self.rect.y < HEIGHT

    class Apple(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            # создание яблкока
            self.image = pygame.Surface((SIZE_BLOCK, SIZE_BLOCK))
            self.image.fill(RED)
            self.rect = self.image.get_rect()
            # добавление случайных координат где будет лежать яблоко
            self.foodx = round(random.randrange(0, WIDTH - SIZE_BLOCK) / 20.0) * 20.0
            self.foody = round(random.randrange(200, HEIGHT - SIZE_BLOCK) / 20.0) * 20.0

        def update(self):
            # генерация яблока в случайном месте
            self.rect.x = self.foodx
            self.rect.y = self.foody

    # создание спрайтов
    all_sprites = pygame.sprite.Group()
    apples = pygame.sprite.Group()
    tails = pygame.sprite.Group()
    snake = Snake()
    all_sprites.add(snake)
    apple = Apple()
    all_sprites.add(apple)
    apples.add(apple)

    snake_list = []
    len_of_snake = 3
    total = 0
    while True:
        clock.tick(FPS)
        screen.fill(FRAME_COLOR)
        all_sprites.draw(screen)
        # проверка нажатия клавиш
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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

        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, WIDTH, 200])
        total_text = courier.render(f'Total: {total}', 0, WHITE)
        speed_text = courier.render(f'Speed: {FPS}', 0, WHITE)
        screen.blit(total_text, (SIZE_BLOCK * 2, 100))
        screen.blit(speed_text, (SIZE_BLOCK + 230, 100))
        # конец игры если змейка вышла за поле
        if not snake.is_inside():
            break

        # проверка координат головы змеи
        snake_head = [snake.rect.x, snake.rect.y]
        snake_list.append(snake_head)

        # если змейка врезается в свой хвост, игра заканчивается
        for x in snake_list[:-1]:
            if x == snake_head:
                break

        collide = pygame.sprite.spritecollide(snake, apples, True)
        # проверка столкновения змейки с яблоком
        # если яблоко было съедено, то змейка начинает расти
        # иначе хвост удаляется
        if collide:
            apple = Apple()
            all_sprites.add(apple)
            apples.add(apple)
            len_of_snake += 1
            total += 2
            FPS += total // 1 + 1
        else:
            snake_list = snake_list[-len_of_snake:]
        snake.update()
        snake.tail(SIZE_BLOCK, snake_list)
        apple.update()
        pygame.display.flip()


menu = pygame_menu.Menu(220, 500, 'Snake',
                        theme=pygame_menu.themes.THEME_ORANGE)

menu.add.text_input('Имя:', default='John Doe')
menu.add.button('Играть', start_the_game)
menu.add.button('Выход', pygame_menu.events.EXIT)

while True:

    screen.blit(bg_img, (19, 68))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()
