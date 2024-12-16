from random import choice

import pygame as pg


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Константы с коодинатами ячеек по x и y
COORDINATES_X = [i * GRID_SIZE for i in range(0, GRID_WIDTH)]
COORDINATES_Y = [i * GRID_SIZE for i in range(0, GRID_HEIGHT)]
# Центр игрового поля
CENTER_FIELD = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

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
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """GameObject является родительским классом для Apple и Snake"""

    def __init__(self):
        self.position = CENTER_FIELD
        self.body_color = None

    def draw(self):
        """Метод draw будет переопределен  в дочерних классах"""


class Apple(GameObject):
    """Apple наследуется от класса GameObject и нужен для создания и отрисовки
    яблока на игровом поле
    """

    def __init__(self, occupied_cells=None):
        """Инициализирует объект apple = Apple()
        :occupied_cells: Принемает на вход список с координатами всех сегментов
        змейки. Координаты по умолчанию это координаты появления змейки
        :body_color:  Цвет яблока
        :position:  Рандомная позиция яблока на игровом поле
        """
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = occupied_cells
        if self.position:
            self.randomize_position(occupied_cells)
        else:
            self.randomize_position([CENTER_FIELD])

    def randomize_position(self, occupied_cells):
        """
        randomize_position генерирует рандомные координаты для  Apple
        на игровом поле
        :occupied_cells: Принимает на вход список позиции змейки
        :return: tuple[int, int]
        """
        dx = list(set(COORDINATES_X) - set([i[0] for i in occupied_cells]))
        dy = list(set(COORDINATES_Y) - set([i[1] for i in occupied_cells]))
        self.position = (
            choice(dx),
            choice(dy))

    def draw(self) -> None:
        """Метод draw отрисовывает Apple на игровом поле"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Snake наследуется от класса GameObject и нужен для создания и отрисовки
    змейки на игровом поле
    :метод: update_direction — обновляет направление движения змейки
    (есть в прекоде).
    :метод: move — обновляет позицию змейки (координаты каждой секции),
    добавляя новую голову в начало списка positions и удаляя последний
    элемент, если длина змейки не увеличилась.
    :метод: draw — отрисовывает змейку на экране, затирая след
    (есть в прекоде).
    :свойство: get_head_position — возвращает позицию головы змейки
    (первый элемент в списке positions).
    :метод: reset — сбрасывает змейку в начальное состояние.
    """

    def __init__(self):
        """
        __init__ — инициализирует начальное состояние змейки.
        :length:  Длина змейки. Изначально змейка имеет длину 1.
        :positions:  Список, содержащий позиции всех сегментов тела
          змейки. Начальная позиция — центр экрана.
        :direction:  Направление движения змейки. По умолчанию змейка
          движется вправо.
        :next_direction:  Следующее направление движения, которое будет
          применено после обработки нажатия клавиши. По умолчанию задать None.
        :body_color:  Цвет змейки. Задаётся RGB-значением
          (по умолчанию — зелёный: (0, 255, 0)).
        """
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = LEFT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Метод отрисовки змейки на игровом поле"""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)
        # Отрисовка головы змейки
        head_rect = pg.Rect(self.get_head_position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    @property
    def get_head_position(self) -> tuple[int, int]:
        """
        Свойство хронящее координаты головы змейки

        :return: positions[0]
        :rtype: tuple[int, int]:
        """
        return self.positions[0]

    def move(self):
        """Метод для просчета движения змейки по игровому полю
        :head_x: Координаты головы по оси SCREEN_WIDTH
        :head_y: Координаты головы по оси SCREEN_HEIGHT
        :direction_x: Напровление движения по оси SCREEN_WIDTH
        :direction_y: Напровление движения по оси SCREEN_HEIGHT
        :Переменные: dx и dy используются для временного хранения координат
        по осям SCREEN_WIDTH и SCREEN_HEIGHT
        """
        head_x, head_y = self.get_head_position
        direction_x, direction_y = self.direction
        dx = (head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH
        dy = (head_y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT
        self.positions.insert(0, (dx, dy))
        if self.length < len(self.positions):
            self.last = self.positions.pop()

    def reset(self):
        """Возвращаем змейку к изначальному состоянию.
        :next_direction: Задаем рандомное напровление движения.
        """
        self.length = 1
        self.positions = [self.position]
        self.next_direction = choice((LEFT, RIGHT, UP, DOWN))
        self.update_direction()
        self.last = None


def main():
    """В данном методе реализована логика игры.
    Создаются и отрисовываются объекты классов Apple() и Snake().
    Проверяется нажатие кнопок и устанавливается направление движения змейки.
    Проверяются столкновения змейки и яблока, а также проверяется столкновение
    змейки с самой собой.
    В случае столкновения змейки с самой собой игра начинается заново.
    """
    # Инициализация pg:
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        # Тут опишите основную логику игры.
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
        apple.draw()
        snake.draw()
        pg.display.update()

# Функция обработки действий пользователя


def handle_keys(game_object):
    """Считывает нажатие конопок на клавиатуре и передает их в метод
    next_direction объекта snake=Snake()
    :param game_object: snake=Snake()
    :type game_object: Snake()
    :raises SystemExit:
    """
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


if __name__ == '__main__':
    main()
