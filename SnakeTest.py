import unittest
from main import Snake


class SnakeTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.possible_directions = ((0, 1), (1, 0), (0, -1), (-1, 0))

    def test_get_size(self):
        snake = Snake([0, 0], 5, 5)
        self.assertEqual(1, snake.get_size())

    def test_grow(self, growth=1):
        snake = Snake([0, 0], 5, 5)
        previous_length = snake.get_size()
        snake.grow(growth)
        current_length = snake.get_size()
        self.assertEqual(previous_length + growth, current_length)

    def test_move(self):
        for direction in self.possible_directions:
            snake = Snake([0, 0], 5, 5, direction)
            snake.move()
            expected = ((direction[0] + 5) % 5, (direction[1] + 5) % 5)
            self.assertEqual(expected, snake.body_segments[0],)

    def test_grow_and_move(self):
        snake = Snake([0, 0], 5, 5)
        snake.grow(2)
        self.assertEqual(3, snake.get_size())
        snake.try_change_direction((0, 1))
        snake.move()
        snake.move()
        snake.move()
        self.assertEqual(snake.body_segments, [(0, 3), (0, 2), (0, 1)])


if __name__ == '__main__':
    unittest.main()
