"""
It is a snake game
Total levels: 10
Each level your start with a snake 4 blocks long
A new obstacle appears on each level
"""

import pygame  # Модуль для написания приложения
import random  # Модуль для того, чтобы фрукты на экране рандомно генерировались в разных позициях
import time


class Snake:
    """ Класс для создания игры """

    def __init__(self):
        """ Инициализируем различные переменные, необходимые для дальнейшей работы приложения """
        super(Snake, self).__init__()

        # Скорость змейки
        self.snake_speed = 20

        # Размер окна с игрой
        self.window_x = 720  # ширина игрового окна
        self.window_y = 480  # высота игрового окна

        # Задаем различные цвета через rgb комбинации
        self.black = pygame.Color(0, 0, 0)  # черный - фон
        self.white = pygame.Color(255, 255, 255)  # белый - очки
        self.red = pygame.Color(255, 0, 0)  # красный
        self.green = pygame.Color(0, 255, 0)  # зеленый - змейка
        self.sky_blue = (0, 255, 255)  # голубой - фрукты
        self.blue = pygame.Color(0, 0, 255)  # синий - окно завершения
        self.orange = (255, 100, 10)  # оранжевый - препятствия

        # Игровые параметры
        pygame.init()  # команда, которая запускает pygame
        pygame.display.set_caption("Snake Game")  # Заголовок (название) игры
        self.game_window = pygame.display.set_mode((self.window_x, self.window_y))  # Создание окна программы
        self.fps = pygame.time.Clock()  # Для того, чтобы игра работала с заданной частотой кадров

        # define snake
        self.snake_position = [100, 50]  # Начальная позиция змейки на экране
        
        # Тело змеи (4 блока)
        self.snake_body = [
            [100, 50],
            [90, 50],
            [80, 50],
            [70, 50]
        ]

        # Переменные для движения
        self.direction = "RIGHT"  # Текущее направление движения змеи
        self.change_to = self.direction  # Переменная для хранения изменения направления

        # Переменные для очков
        self.scores = 0
        self.score_font = pygame.font.SysFont("times new roman", 20)
        self.score_surface = self.score_font.render(f"Scores: {str(self.scores)}", True, self.white)
        self.score_rect = self.score_surface.get_rect()
        self.game_window.blit(self.score_surface, self.score_rect)
        self.font = 'times new roman'
        self.size = 20

        # Работа с текстом для окна завершения программы (Число очков, уровень)
        self.text = ""
        self.end_game_font = pygame.font.SysFont('times new roman', 50)
        self.game_over_surface_score = self.end_game_font.render(
            'Your Score is : ' + str(self.scores), True, self.red)
        self.game_over_rect = self.game_over_surface_score.get_rect()
        self.game_over_surface_level = self.end_game_font.render(
            'Your Score is : ' + str(self.scores), True, self.red)
        self.game_over_rect = self.game_over_surface_level.get_rect()

        # Определяем массив для препятствий и переменную для текущего уровня в игре
        self.obstacle_body = []
        self.level = 0
        self.check = 1

        # Создаем фрукт и располагаем его случайным образом на экране
        while True:
            self.fruit_position = [
                random.randrange(1, (self.window_x // 10)) * 10,
                random.randrange(1, (self.window_y // 10)) * 10
            ]
            if self.fruit_position not in self.obstacle_body:
                break
        self.fruit_spawn = True

    def game(self):
        """ Функция, отвечающая за основную работу с игрой """
        while True:
            # Заполняем экран черным цветом
            self.game_window.fill(self.black)

            # Если сменился уровень, то меняем направление движения змеи вправо, чтоб она не врезалась ни во что в начале игры
            if self.check == 0:
                self.change_to = 'RIGHT'
                self.direction = 'RIGHT'
                self.check += 1

            # Обработка нажатий пользователя
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.change_to = 'UP'
                    elif event.key == pygame.K_DOWN:
                        self.change_to = 'DOWN'
                    elif event.key == pygame.K_LEFT:
                        self.change_to = 'LEFT'
                    elif event.key == pygame.K_RIGHT:
                        self.change_to = 'RIGHT'
                elif event.type == pygame.QUIT:
                    self.game_over()

            # Исключаем ошибки нажатий (Например, когда змея движется вверх, а пользователь нажимает вниз)
            if self.change_to == 'UP' and self.direction != 'DOWN':
                self.direction = 'UP'
            elif self.change_to == 'DOWN' and self.direction != 'UP':
                self.direction = 'DOWN'
            elif self.change_to == 'LEFT' and self.direction != 'RIGHT':
                self.direction = 'LEFT'
            elif self.change_to == 'RIGHT' and self.direction != 'LEFT':
                self.direction = 'RIGHT'

            # Изменяем направление движения змеи в соответствии с пользовательским нажатием
            if self.direction == 'UP':
                self.snake_position[1] -= 10
            elif self.direction == 'DOWN':
                self.snake_position[1] += 10
            elif self.direction == 'LEFT':
                self.snake_position[0] -= 10
            elif self.direction == 'RIGHT':
                self.snake_position[0] += 10

            # Увеличиваем длину змеи после того, как она съела фрукт
            self.snake_body.insert(0, list(self.snake_position))
            if self.snake_position[0] == self.fruit_position[0] and self.snake_position[1] == self.fruit_position[1]:
                self.scores += 10 # Прибавляем 10 очков за каждый съеденный фрукт
                self.snake_body.insert(0, list(self.snake_position))
                self.fruit_spawn = False
                continue
            else:
                self.snake_body.pop()

            # Рисуем змею на экране
            for i, pos in enumerate(self.snake_body):
                pygame.draw.rect(self.game_window, self.green,
                                 pygame.Rect(pos[0], pos[1], 10, 10))

            # Смена уровня при достижении 50 очков
            self.check += 1
            if self.scores == 50:
                self.check = 0
                self.snake_position = [100, 50] # Возвращаем размер змеи в изначальный
                self.snake_body = [
                    [100, 50],
                    [90, 50],
                    [80, 50],
                    [70, 50]
                ]
                self.level += self.scores
                self.scores = 0
                self.snake_speed = 20
                time.sleep(2)  # Пауза между уровнями
                self.change_to = 'RIGHT' # Меняем направление движения
                self.direction = 'RIGHT'

            # Создаем препятствия
            self.generate_obstacle_levels()
            for i, pos in enumerate(self.obstacle_body):
                pygame.draw.rect(self.game_window, self.orange,
                                 pygame.Rect(pos[0], pos[1], 10, 10))

            # Генерируем новую позицию для фрукта
            if not self.fruit_spawn:
                while True:
                    self.fruit_position = [
                        random.randrange(1, (self.window_x // 10)) * 10,
                        random.randrange(1, (self.window_y // 10)) * 10
                    ]
                    if self.fruit_position not in self.obstacle_body:
                        break
            self.fruit_spawn = True

            # Рисуем фрукт
            pygame.draw.rect(self.game_window, self.sky_blue, pygame.Rect(
                self.fruit_position[0], self.fruit_position[1], 10, 10))

            # Позволяем змее телепортироваться (проходить через верхний экран и оказываться внизу)
            self.snake_position[0] %= self.window_x
            self.snake_position[1] %= self.window_y

            # Завершаем уровень если змея коснулась сама себя
            if self.snake_position in self.snake_body[1:] or self.snake_position in self.obstacle_body:
                self.game_over()

            # Обновляем экран
            self.show_scores()
            pygame.display.update()
            self.fps.tick(self.snake_speed)

    def game_over(self):
        """ Функция завершения игры """
        # Определяем стиль текста
        self.end_game_font = pygame.font.SysFont('times new roman', 50)

        # Создаем текст
        if self.level != 550:  # Если не последний уровень - показываем уровень и количество очков
            self.text = f"Your level is : {str((self.level // 50) + 1)}"
        else:  # Если последний - Показываем количество очков и сообщение "Игра пройдена"
            self.text = "Game completed"
        self.game_over_surface_score = self.end_game_font.render(
            f"Your total score is : " + str(self.level + self.scores), True, self.blue)
        self.game_over_surface_level = self.end_game_font.render(
            self.text, True, self.blue)

        # Определяем область для расположения текста
        self.game_over_rect = self.game_over_surface_score.get_rect()
        self.game_over_rect.midtop = (self.window_x / 2, self.window_y / 4)
        self.game_window.blit(self.game_over_surface_score, self.game_over_rect)
        self.game_over_rect = self.game_over_surface_level.get_rect()
        self.game_over_rect.midtop = (self.window_x / 2, self.window_y / 4 + 50)

        # Добавляем текст на экран
        self.game_window.blit(self.game_over_surface_level, self.game_over_rect)
        pygame.display.flip()
        time.sleep(1.5)
        pygame.quit()
        quit()

    def show_scores(self):
        """ Функция для обновления количества очков """
        self.score_font = pygame.font.SysFont(self.font, self.size)
        self.score_surface = self.score_font.render(
            f"Scores: {str(self.scores)}   |   Level: {str((self.level // 50) + 1)}", True, self.white)
        self.score_rect = self.score_surface.get_rect()
        self.game_window.blit(self.score_surface, self.score_rect)

    def generate_obstacle_levels(self):
        """ Функция для создания препятствий в соответствии с текущим уровнем """
        if self.level == 50:
            # level 1
            for j in range(0, 20, 10):
                for i in range(140, 340, 10):
                    self.obstacle_body.append([100 + j, i])

        elif self.level == 100:
            # level 2
            for j in range(0, 20, 10):
                for i in range(140, 340, 10):
                    self.obstacle_body.append([self.window_x - 100 - j, i])

        elif self.level == 150:
            # level 3
            for j in range(0, 20, 10):
                for i in range(80, 200, 10):
                    self.obstacle_body.append([200 + j, i])

        elif self.level == 200:
            # level 4
            for j in range(0, 20, 10):
                for i in range(80, 200, 10):
                    self.obstacle_body.append([200 + j, self.window_y - i])

        elif self.level == 250:
            # level 5
            for j in range(0, 20, 10):
                for i in range(80, 200, 10):
                    self.obstacle_body.append([self.window_x - 200 - j, self.window_y - i])

        elif self.level == 300:
            # level 6
            for j in range(0, 20, 10):
                for i in range(80, 200, 10):
                    self.obstacle_body.append([self.window_x - 200 - j, i])

        elif self.level == 350:
            # level 7
            for j in range(0, 20, 10):
                for i in range(200, 340, 10):
                    self.obstacle_body.append([i, 80 + j])

        elif self.level == 400:
            # level 8
            for j in range(0, 20, 10):
                for i in range(200, 340, 10):
                    self.obstacle_body.append([self.window_x - i, 80 + j])

        elif self.level == 450:
            # level 9
            for j in range(0, 20, 10):
                for i in range(200, 340, 10):
                    self.obstacle_body.append([self.window_x - i, self.window_y - 80 - j])

        elif self.level == 500:
            # level 10
            for j in range(0, 20, 10):
                for i in range(200, 340, 10):
                    self.obstacle_body.append([i, self.window_y - 80 - j])

        elif self.level == 550:
            self.game_over()


if __name__ == "__main__":
    snake = Snake()
    snake.game()
