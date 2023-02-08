from data import Point
from enum import Enum
from random import Random


class MovingDir(str, Enum):
    UP = 'up'
    DOWN = 'down'
    RIGHT = 'right'
    LEFT = 'left'


class GameState(Enum):
    ABORTED = 'aborted'
    RUNNING = 'running'
    WON = 'won'
    LOST = 'lost'


class SnakeGame:
    def __init__(self, size):
        self.__size = size
        self.__snake = [Point(1, 0), Point(0, 0)]
        self.__moving_dir = MovingDir.RIGHT
        self.__food = Point(2, 0)
        self.__rng = Random()
        self.__state = GameState.RUNNING

    def process_input(self, input):
        if not isinstance(input, str):
            return
        # process moving direction
        if hasattr(MovingDir, input.upper()):
            # TODO: reject opposite directions
            self.__moving_dir = MovingDir(input)

    def advance(self):
        # Only advance game when it is running.
        if self.__state != GameState.RUNNING:
            return

        moving_dir = self.__moving_dir
        snake_array = self.__snake
        width = self.__size.X
        height = self.__size.Y

        # Add a new head in the snake's moving direction,
        # teleport to the opposite side if the head is at the border.
        head = snake_array[0].copy()
        if moving_dir == MovingDir.RIGHT:
            if head.X == width - 1:
                head.X = 0
            else:
                head.X += 1
        elif moving_dir == MovingDir.LEFT:
            if head.X == 0:
                head.X = width - 1
            else:
                head.X -= 1
        elif moving_dir == MovingDir.DOWN:
            if head.Y == height - 1:
                head.Y = 0
            else:
                head.Y += 1
        elif moving_dir == MovingDir.UP:
            if head.Y == 0:
                head.Y = height - 1
            else:
                head.Y -= 1
        snake_array.insert(0, head)

        # Remove the tail piece, except when the snake eats the food.
        if snake_array[0] != self.__food:
            snake_array.pop()
        else:
            # Game is won when the snake fills the entire playing area
            if len(snake_array) >= width * height:
                self.__state = GameState.WON
            # Spawn new food.
            else:
                self.__food = self.create_food()

        # Game is lost when the snake's head collides with its body.
        if snake_array[0] in snake_array[1:]:
            self.__state = GameState.LOST

    def create_food(self):
        width = self.__size.X
        height = self.__size.Y
        snake_array = self.__snake

        while True:
            # Spawn food in a random position that is not occupied by a snake piece
            food = Point(self.__rng.randrange(0, width),
                         self.__rng.randrange(0, height))
            if not food in snake_array:
                break

        return food

        # choices = height * width - len(snake_array)
        # food_index = self.__rng.randrange(0, choices)
        # sorted_snake = snake_array.copy()
        # sorted_snake.sort()
        # for i in range(len(sorted_snake)):
        #     piece_index = (height * sorted_snake[i].X) + sorted_snake[i].Y
        #     if piece_index <= food_index:
        #         food_index += 1

        # food = Point(food_index // height, food_index % height)
        # return food

    def get_size(self):
        return self.__size

    def get_food(self):
        return self.__food

    def get_snake(self):
        return self.__snake

    def get_state(self):
        return self.__state
