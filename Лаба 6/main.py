import pygame
import random
from queue import PriorityQueue

# Инициализация графического движка
pygame.init()
pygame.font.init()

# Константы игрового окна и сетки
WIDTH = 600
GRID_SIZE = 10  # Фиксированный размер сетки 10х10 для лабораторной работы
CELL_SIZE = WIDTH // GRID_SIZE
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Алгоритм А* (Вариант 21)")

# Шрифт для отрисовки текстовых значений весов
FONT = pygame.font.SysFont('Arial', 14)

# Цветовая палитра компонентов (RGB)
WHITE = (255, 255, 255)       # Свободная ячейка (базовый вес = 1)
BLACK = (0, 0, 0)             # Статическая стена / препятствие
GREY = (128, 128, 128)        # Линии разметки сетки
ORANGE = (255, 165, 0)        # Стартовая ячейка (Корона)
TURQUOISE = (64, 224, 208)    # Целевая ячейка (Крестик)
GREEN = (0, 255, 0)           # Открытый список (ячейки в очереди)
RED = (255, 0, 0)             # Закрытый список (посещенные ячейки)
PURPLE = (128, 0, 128)        # Результирующий кратчайший путь

# Карта соответствия весов и оттенков ячеек (для взвешенного графа)
WEIGHT_COLORS = {
    1: (255, 255, 255),
    2: (240, 240, 210),
    3: (220, 220, 170),
    4: (190, 190, 130),
    5: (160, 160, 90)
}

class Cell:
    def __init__(self, row, col):
        self.row = row  # Индекс строки матрицы
        self.col = col  # Индекс столбца матрицы
        self.x = col * CELL_SIZE  # Экранная координата X
        self.y = row * CELL_SIZE  # Экранная координата Y
        self.color = WHITE
        self.weight = 1  # Базовая стоимость прохода через ячейку
        self.neighbors = []  # Список смежных доступных ячеек

    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    # Сброс параметров к исходным значениям
    def reset(self):
        self.color = WHITE
        self.weight = 1

    # Методы смены цвета / состояния
    def make_start(self):
        self.color = ORANGE

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_open(self):
        if self.color not in [ORANGE, TURQUOISE]:
            self.color = GREEN

    def make_closed(self):
        if self.color not in [ORANGE, TURQUOISE]:
            self.color = RED

    def make_path(self):
        if self.color not in [ORANGE, TURQUOISE]:
            self.color = PURPLE

    def draw(self, win):
        # Визуализация взвешенных клеток (с выводом значения веса на экран)
        if self.color == WHITE and self.weight > 1:
            pygame.draw.rect(win, WEIGHT_COLORS[self.weight], (self.x, self.y, CELL_SIZE, CELL_SIZE))
            text_surface = FONT.render(f"w:{self.weight}", True, (50, 50, 50))
            win.blit(text_surface, (self.x + 15, self.y + 15))
        else:
            pygame.draw.rect(win, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))

def update_neighbors(self, grid):
        # Поиск доступных соседей (без учета стен)
        self.neighbors = []
        # Проверка направления Вниз
        if self.row < GRID_SIZE - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Проверка направления Вверх
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # Проверка направления Вправо
        if self.col < GRID_SIZE - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Проверка направления Влево
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

def h(p1, p2):
    # Расчет эвристической функции (Манхэттенское расстояние)
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw_fn):
    # Обратный обход графа от финиша к старту для генерации пути
 while current in came_from:
        current = came_from[current]
        current.make_path()
        draw_fn()

def a_star_algorithm(draw_fn, grid, start, end):
    count = 0  # Идентификатор для разрешения коллизий при равных f_score
    open_set = PriorityQueue()
    
    # Заносим стартовую вершину в приоритетную очередь
    open_set.put((0, count, start))
    came_from = {} 
    
    # g_score: массивы стоимостей пути от старта (по умолчанию бесконечны)
    g_score = {cell: float("inf") for row in grid for cell in row}
    g_score[start] = 0  
    # f_score: полная оценочная стоимость пути (g_score + эвристика h)
    f_score = {cell: float("inf") for row in grid for cell in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    # Хэш-таблица для мгновенного поиска элементов, находящихся внутри open_set
    open_set_hash = {start}
    while not open_set.empty():
        # Обработка прерывания работы во время выполнения алгоритма
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        # Извлечение вершины с минимальным значением f_score
        current = open_set.get()[2]
        open_set_hash.remove(current)

        # Условие успешного завершения алгоритма
        if current == end:
            reconstruct_path(came_from, end, draw_fn)
            end.make_end()
            start.make_start()
            return True 
        # Обход смежных соседей текущей вершины
        for neighbor in current.neighbors:
            # Новая стоимость g включает индивидуальный вес целевой ячейки
            temp_g_score = g_score[current] + neighbor.weight

            # Проверка: найден ли более оптимальный путь к соседу
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                
  	# Добавление соседа в очередь, если его там нет
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        # Отрисовка
        draw_fn()

        if current != start:
            current.make_closed()

    return False

def make_grid():
    # Инициализация и заполнение двумерной структуры игрового поля
    grid = []
    for i in range(GRID_SIZE):
        grid.append([])
        for j in range(GRID_SIZE):
            cell = Cell(i, j)
            grid[i].append(cell)
    return grid
def load_variant_21(grid):
    # Генерация варианта №21
    for row in grid:
        for cell in row:
            cell.reset()

    # Точки старта и финиша из задания (Вариант 21)
    start = grid[3][0]  # Корона (строка 3, столбец 0)
    end = grid[9][9]    # Крестик (строка 9, столбец 9)
    start.make_start()
    end.make_end()

    # Список координат статических препятствий согласно схеме
    barriers = [
        (0, 3),
        (1, 3), (1, 6),
        (2, 3),
        (3, 1), (3, 2),
        (4, 7), (4, 8),
        (5, 0), (5, 1), (5, 4), (5, 6), (5, 8),
        (6, 4), (6, 6), (6, 7), (6, 9),
        (7, 1), (7, 2), (7, 4), (7, 5), (7, 6),
        (8, 1), (8, 2),
        (9, 1), (9, 2), (9, 4), (9, 5)
]
    for r, c in barriers:
        grid[r][c].make_barrier()

    return start, end

def generate_random_map(grid, weighted=False):
    # Случайная генерация поля / взвешенной карты с препятствиями
    for row in grid:
        for cell in row:
            cell.reset()
            # Назначение случайной стоимости прохода для взвешенного режима
            if weighted:
                cell.weight = random.randint(1, 5)

    # Выбор случайных непересекающихся координат старта и финиша
    start_row, start_col = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
    end_row, end_col = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)

    while (start_row, start_col) == (end_row, end_col):
        end_row, end_col = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)

    start = grid[start_row][start_col]
    end = grid[end_row][end_col]
    start.weight = 1
    end.weight = 1

    start.make_start()
    end.make_end()

    # Заполнение 20% свободного пространства случайными стенами
    obstacle_count = int(GRID_SIZE * GRID_SIZE * 0.2)
    for _ in range(obstacle_count):
        r, c = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        if not grid[r][c].is_start() and not grid[r][c].is_end():
            grid[r][c].make_barrier()

    return start, end

def draw(win, grid):
    # Функция комплексной отрисовки интерфейса приложения
    win.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.draw(win)

    # Отрисовка координатных линий сетки поверх ячеек

    for i in range(GRID_SIZE + 1):
        pygame.draw.line(win, GREY, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
        pygame.draw.line(win, GREY, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH))

    pygame.display.update()

def main():
    grid = make_grid()
    start, end = load_variant_21(grid)
    run = True

    # Консольный вывод карты управления приложениестом
    print("Управление:")
    print("SPACE - Запуск визуализации алгоритма А*")
    print("V     - Сбросить карту на Вариант №21")
    print("R     - Сгенерировать СЛУЧАЙНОЕ ПОЛЕ (без весов)")
    print("W     - Сгенерировать СЛУЧАЙНУЮ КАРТУ С ВЕСАМИ ячеек")

    while run:
        draw(WIN, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

# Диспетчеризация событий клавиатуры
            if event.type == pygame.KEYDOWN:
                # По нажатию SPACE обновляем список соседей у ячеек и запускаем алгоритм
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)
                    a_star_algorithm(lambda: draw(WIN, grid), grid, start, end)

                if event.key == pygame.K_v:
                    start, end = load_variant_21(grid)

                if event.key == pygame.K_r:
                    start, end = generate_random_map(grid, weighted=False)

                if event.key == pygame.K_w:
                    start, end = generate_random_map(grid, weighted=True)

    pygame.quit()

if __name__ == "__main__":
    main()
