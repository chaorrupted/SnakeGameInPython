from random import randrange
from operator import add


class Snake:

    def __init__(self, starting_position, row, column, starting_direction=(0, 1)):
        self.direction = starting_direction
        self.row = row
        self.column = column
        self.body_segments = [starting_position]
        self.possible_directions = ((0, 1), (0, -1), (1, 0), (-1, 0))

    def get_size(self):
        return len(self.body_segments)

    def grow(self, length=1):
        for _ in range(0, length):
            self.body_segments.append(self.body_segments[-1])

    def move(self) -> bool:
        next_cell = tuple(map(add, self.body_segments[0], self.direction))
        next_cell = (next_cell[0] % self.row, next_cell[1] % self.column)
        if next_cell in self.body_segments:
            if next_cell == self.body_segments[-1]:
                if self.body_segments[-1] != self.body_segments[-2]:
                    self.move_to_next_cell(next_cell)
                    return True
            return False
        else:
            self.move_to_next_cell(next_cell)
            return True

    def move_to_next_cell(self, next_cell):
        for i in reversed(range(0, len(self.body_segments))):
            if i == 0:
                self.body_segments[i] = next_cell
            else:
                self.body_segments[i] = self.body_segments[i - 1]

    def try_change_direction(self, new_direction):
        opposite_direction = (-self.direction[0], -self.direction[1])
        if new_direction != opposite_direction:
            self.direction = new_direction


class Board:

    def __init__(self, row=5, column=5):
        self.row = row
        self.column = column
        self.board = [["-" for i in range(0, self.row)] for k in range(0, self.column)]
        self.food_places_and_powers = {}

    def draw_board(self):
        for row in self.board:
            for cell in row:
                print(cell, end=" ")
            print()
        print()

    def place_snake(self, row, column):
        self.board[row][column] = "S"

    def place_food(self):
        for position in self.food_places_and_powers:
            self.board[position[0]][position[1]] = "F"

    def add_food(self, row, column, power=1):
        self.food_places_and_powers[(row, column)] = power

    def clear_cell(self, row, column):
        self.board[row][column] = "-"

    def clear_board(self):
        self.board = [["-" for i in range(0, self.row)] for k in range(0, self.column)]


class GameManager:

    def __init__(self, rows=5, columns=5, snake_starting_position=(0, 0)):
        self.game_over = False
        self.board = Board(rows, columns)
        self.snake = Snake(snake_starting_position, rows, columns)
        self.score = 0

    def generate_food(self):
        random_position = (randrange(0, self.board.row), randrange(0, self.board.column))
        tries = 0
        while random_position in self.snake.body_segments and tries < 20:
            random_position = (randrange(0, self.board.row), randrange(0, self.board.column))
            tries += 1

        if tries < 20:
            self.board.add_food(random_position[0], random_position[1])
        else:
            # if board is almost full, hand-pick empty spaces to place food. if board is full, stop game, congratulate player
            pass

    def update_and_draw_board(self):
        self.board.clear_board()
        self.board.place_food()
        for segment in self.snake.body_segments:
            self.board.place_snake(segment[0], segment[1])
        self.board.draw_board()

    def start(self):
        self.generate_food()
        self.update_and_draw_board()
        while not self.game_over:
            self.take_input_and_update_snake_direction()
            move_successful = self.snake.move()
            if move_successful:
                self.check_and_eat_food()
                self.update_and_draw_board()
            else:
                self.game_over = True
                print(f"you hit your own tail. Your score: {self.score}")

    def check_and_eat_food(self):
        if self.snake.body_segments[0] in self.board.food_places_and_powers:
            self.snake.grow(self.board.food_places_and_powers[self.snake.body_segments[0]])
            self.score += self.board.food_places_and_powers[self.snake.body_segments[0]]
            del self.board.food_places_and_powers[self.snake.body_segments[0]]
            self.generate_food()

    def take_input_and_update_snake_direction(self):
        inp = str(input("hit Enter to take one game step. type w, a, s, or d to change direction."))
        if inp == "d":
            self.snake.try_change_direction((0, 1))
        elif inp == "a":
            self.snake.try_change_direction((0, -1))
        elif inp == "w":
            self.snake.try_change_direction((-1, 0))
        elif inp == "s":
            self.snake.try_change_direction((1, 0))
        else:
            pass


if __name__ == "__main__":
    game_manager = GameManager()

    game_manager.start()
