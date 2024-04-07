from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Центр экрана
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject:
    """Базовый класс игровых объектов."""

    position = SCREEN_CENTER

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        self.body_color = body_color

    def draw(self):
        """Отрисовка объекта"""
        pass


class Apple(GameObject):
    """Класс описывающией яблоко и действия с ним."""

    def __init__(self, body_color=APPLE_COLOR):
        self.position = self.randomize_position()
        super().__init__(body_color)

    def randomize_position(self):
        """Возвращает рандомную позицию"""
        return (randint(0, GRID_WIDTH - GRID_SIZE) * GRID_SIZE,
                randint(0, GRID_HEIGHT - GRID_SIZE) * GRID_SIZE)

    def draw(self):
        """Отрисовывает яблоко"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс описывающий змею, ее отрисовку и движение"""

    direction = RIGHT
    next_direction = None
    length = 1
    positions = [SCREEN_CENTER]

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.last = None

    def draw(self):
        """Отрисовывает змею"""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает координаты головы змеи"""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки и удаляет последний элемент"""
        curreny_head_x, current__head_y = self.get_head_position()
        direction_x, direction_y = self.direction

        new_head_x = curreny_head_x + direction_x * GRID_SIZE
        new_head_y = current__head_y + direction_y * GRID_SIZE

        head_x = (new_head_x - SCREEN_WIDTH if new_head_x >= SCREEN_WIDTH else
                  (SCREEN_WIDTH + new_head_x if new_head_x < 0
                   else new_head_x))
        head_y = (new_head_y - SCREEN_HEIGHT if
                  new_head_y >= SCREEN_HEIGHT else
                  (SCREEN_HEIGHT + new_head_y if new_head_y < 0
                   else new_head_y))

        head_position = (head_x, head_y)

        if any(item == head_position for item in self.positions):
            self.reset()
        else:
            self.positions.insert(0, head_position)

            if len(self.positions) > self.length:
                self.last = self.positions.pop()

    def reset(self):
        """Возвращает змейку к изначальным параметрам"""
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = choice([RIGHT, LEFT, DOWN, UP])


def main():
    """Основной цикл игры с отрисовкой змейки и яблока"""
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()

            while any(item == apple.position for item in snake.positions):
                apple.position = apple.randomize_position()

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
