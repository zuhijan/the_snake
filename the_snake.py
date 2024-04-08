from random import choice, randint

import pygame as pg

# Инициализация PyGame:
pg.init()

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
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


def get_random_position():
    """Возвращает рандомную позицию"""
    return (randint(0, GRID_WIDTH - GRID_SIZE) * GRID_SIZE,
            randint(0, GRID_HEIGHT - GRID_SIZE) * GRID_SIZE)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        self.body_color = body_color
        self.position = SCREEN_CENTER

    def draw(self):
        """Отрисовка объекта"""


class Apple(GameObject):
    """Класс описывающией яблоко и действия с ним."""

    def __init__(self, snake_positions=[SCREEN_CENTER],
                 body_color=APPLE_COLOR):
        self.randomize_position(snake_positions)
        super().__init__(body_color)

    def randomize_position(self, snake_positions):
        """Возвращает рандомную позицию"""
        self.position = get_random_position()
        while any(item == self.position for item in snake_positions):
            self.position = get_random_position()

    def draw(self):
        """Отрисовывает яблоко"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс описывающий змею, ее отрисовку и движение"""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.positions = [SCREEN_CENTER]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
        self.last = None

    def draw(self):
        """Отрисовывает змею"""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

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
        current_head_x, current_head_y = self.get_head_position()
        direction_x, direction_y = self.direction

        head_x = ((current_head_x + (direction_x * GRID_SIZE))
                  % SCREEN_WIDTH)
        head_y = ((current_head_y + (direction_y * GRID_SIZE))
                  % SCREEN_HEIGHT)

        head_position = (head_x, head_y)
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
            apple.randomize_position(snake.positions)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if any(item == snake.get_head_position() for
               item in snake.positions[2:]):
            snake.reset()

        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
