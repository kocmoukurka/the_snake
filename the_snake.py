from random import randint

import pygame


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
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """GameObject является родительским классом для Apple и Snake"""

    def __init__(self):
        self.position = (
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Метод draw будет переопределен  в дочерних классах"""
        pass


class Apple(GameObject):
    """Apple наследуется от класса GameObject и нужен для создания и отрисовки
    яблока на игровом поле
    """

    def __init__(self):
        """Инициализирует объект apple = Apple()
        :свойство: body_color цвет яблока
        :свойство: position рандомная позиция яблока на игровом поле
        """
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """
        randomize_position генерирует рандомные координаты для  Apple
        на игровом поле

        :return: tuple[int, int]
        """
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self) -> None:
        """Метод draw отрисовывает Apple на игровом поле"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


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
        :свойство: length — длина змейки. Изначально змейка имеет длину 1.
        :свойство: positions — список, содержащий позиции всех сегментов тела
          змейки. Начальная позиция — центр экрана.
        :свойство: direction — направление движения змейки. По умолчанию змейка
          движется вправо.
        :свойство: next_direction — следующее направление движения, которое
        будет
          применено после обработки нажатия клавиши. По умолчанию задать None.
        :свойство: body_color — цвет змейки. Задаётся RGB-значением
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

    def draw(self):
        """Метод отрисовки змейки на игровом поле"""
        for position in self.positions[:-1]:
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
        :Словарь: transition_by_x словарь для получения координат
        по оси SCREEN_WIDTH при пересечении границ игрового поля
        :Словарь: transition_by_y словарь для получения координат
        по оси SCREEN_HEIGHT при пересечении границ игрового поля
        :Переменные: dx и dy используются для временного хранения координат
        по осям SCREEN_WIDTH и SCREEN_HEIGHT и проверки пересечения границы
        игрового поля
        """
        transition_by_x = {0: 620, 620: 0}
        transition_by_y = {0: 460, 460: 0}
        dx, dy = tuple(
            int((self.get_head_position[i]
                // GRID_SIZE + self.direction[i]) * GRID_SIZE) for i in [0, 1])
        if dx < 0 or dx > 620:
            dx = transition_by_x[self.positions[0][0]]
        if dy < 0 or dy > 460:
            dy = transition_by_y[self.positions[0][1]]
        self.positions.insert(0, (dx, dy))
        if self.length < len(self.positions):
            self.last = self.positions.pop()

    def reset(self):
        """Вызывает метод __init__() для сброса змейки в случае смерти к
        стартовым координатам и длине тела
        """
        self.__init__()


def main():
    """В данном методе реализована логика игры.
    Создаются и отрисовываются объекты классов Apple() и Snake().
    Проверяется нажатие кнопок и устанавливается направление движения змейки.
    Проверяются столкновения змейки и яблока,а
    также проверяется столкновение змейки с собой,
    в случае столкновения змейки с самой собой игра начинается заново.
    """
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    while True:
        # Тут опишите основную логику игры.
        clock.tick(4)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.__init__()
        if snake.positions[0] in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
        apple.draw()
        snake.draw()
        pygame.display.update()

# Функция обработки действий пользователя


def handle_keys(game_object):
    """Считывает нажатие конопок на клавиатуре и передает их в метод
    next_direction объекта snake=Snake()
    :param game_object: snake=Snake()
    :type game_object: Snake()
    :raises SystemExit:
    """
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


if __name__ == '__main__':
    main()
