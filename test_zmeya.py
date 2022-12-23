import unittest
import snake_game


class SnakeTest(unittest.TestCase):
    def test_game_creation(self):
        snake = snake_game.Snake()
        self.assertTrue(snake is not None)

    def test_snake_level_generate(self):
        snake = snake_game.Snake()
        for i in [50, 100, 150]:
            snake.level = i
            self.assertTrue(snake.generate_obstacle_levels() is None)

