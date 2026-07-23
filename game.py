#!venv/bin/python
from utils.cell_types import Cell
from utils.mov_dirs import Movdir
from utils.mov_res import Movres
import random
import numpy as np
from collections import deque


# directions are up, left, down, right. equal to 0, 1, 2, 3.
def are_there_walls(x, y, dim):
    res = [False for i in range(4)]
    if (y == 0):
        res[0] = True
    elif (y == dim - 1):
        res[2] = True
    if (x == 0):
        res[1] = True
    elif (x == dim - 1):
        res[3] = True
    return res


def are_opposing(dir1, dir2):
    if ((dir1 + 2) % 4 == dir2):
        return True
    return False


def generate_init_snake_coords(dim):
    res = []
    x_start = random.randrange(dim)
    y_start = random.randrange(dim)
    res.append([x_start, y_start])
    where_walls = are_there_walls(x_start, y_start, dim)
    second_chunk_dir = random.randrange(4)
    while (where_walls[second_chunk_dir]):
        second_chunk_dir = random.randrange(4)
    match second_chunk_dir:
        case 0:
            res.append([res[0][0], res[0][1] - 1])
        case 1:
            res.append([res[0][0] - 1, res[0][1]])
        case 2:
            res.append([res[0][0], res[0][1] + 1])
        case 3:
            res.append([res[0][0] + 1, res[0][1]])
    last_dir = random.randrange(4)
    where_walls = are_there_walls(res[1][0], res[1][1], dim)
    while (are_opposing(last_dir, second_chunk_dir)
            or (where_walls[last_dir])):
        last_dir = random.randrange(4)
    match last_dir:
        case 0:
            res.append([res[1][0], res[1][1] - 1])
        case 1:
            res.append([res[1][0] - 1, res[1][1]])
        case 2:
            res.append([res[1][0], res[1][1] + 1])
        case 3:
            res.append([res[1][0] + 1, res[1][1]])
    return res


def symbolize_cell(cell_enum, is_general=True):
    match cell_enum:
        case Cell.EMPTY:
            if (is_general):
                return " "
            else:
                return "0"
        case Cell.WALL:
            return "W"
        case Cell.HEAD:
            return "H"
        case Cell.BODY:
            return "S"
        case Cell.GREEN_APPLE:
            return "G"
        case Cell.RED_APPLE:
            return "R"
    return "-"


class Game:
    """Describes the game field. Can act on it, can return general info"""
    dimension = 10
    size = dimension + 2

    def gen_apples(self, count, kind):
        for i in range(count):
            x_pick = random.randrange(1, self.dimension + 1)
            y_pick = random.randrange(1, self.dimension + 1)
            attempts = 0
            while (self.board[x_pick + y_pick*self.size] != Cell.EMPTY):
                x_pick = random.randrange(1, self.dimension + 1)
                y_pick = random.randrange(1, self.dimension + 1)
                attempts += 1
                if (attempts >= 2000):
                    raise Exception("Too many apple placement attemps; "
                                    "board too crowded?")
            self.board[x_pick + y_pick*self.size] = kind

    def __init__(self):
        #   x - >
        # y  0  1  2  3  4  5  6  7  8  9 10 11
        # | 12 13 14 15 16 17 18 19 20 21 22 23
        # v
        #
        # so, to get x: % self.size
        # to get y: / self.size
        #
        # from xy to i then:
        # i = x + y*self.size
        self.board = [
            Cell.EMPTY if (
                (i % self.size != 0)
                and (i % self.size != self.size - 1)
                and (i > self.size)
                and (i < self.size*(self.size - 1)))
            else Cell.WALL for i in range(self.size*self.size)]
        # use numpy just for that sweet +1
        self.snake = np.array(generate_init_snake_coords(self.dimension)) + 1
        # use a deque cuz it flows better with pop/push
        self.snake = deque(list(part) for part in self.snake)
        ctr = 0
        for xy_pair in self.snake:
            if (ctr == 0):
                self.board[xy_pair[0] + xy_pair[1]*self.size] = Cell.HEAD
            else:
                self.board[xy_pair[0] + xy_pair[1]*self.size] = Cell.BODY
            ctr += 1
        self.gen_apples(1, Cell.RED_APPLE)
        self.gen_apples(2, Cell.GREEN_APPLE)

    def process_move(self, to_where, erase_in_back):
        my_head = self.snake[0]
        self.board[my_head[0] + my_head[1]*self.size] = Cell.BODY
        self.snake.appendleft(to_where)
        self.board[to_where[0] + to_where[1]*self.size] = Cell.HEAD
        for i in range(erase_in_back):
            popped = self.snake.pop()
            self.board[popped[0] + popped[1]*self.size] = Cell.EMPTY

    def move_checker(self, axis, sign):
        my_head = self.snake[0]
        next_tile_coords = my_head.copy()
        next_tile_coords[axis] += sign
        next_tile = self.board[
            next_tile_coords[0] + next_tile_coords[1]*self.size
        ]
        match next_tile:
            case Cell.EMPTY:
                self.process_move(next_tile_coords, 1)
                self.result = Movres.NORMAL
            case Cell.WALL:
                self.process_move(next_tile_coords, 1)
                self.result = Movres.DEAD
            case Cell.HEAD:
                self.result = Movres.UNKNOWN
                raise Exception("Met your own head. Something is not working")
            case Cell.BODY:
                self.process_move(next_tile_coords, 1)
                self.result = Movres.DEAD
            case Cell.GREEN_APPLE:
                self.process_move(next_tile_coords, 0)
                self.gen_apples(1, Cell.GREEN_APPLE)
                self.result = Movres.GOOD_APPLE
            case Cell.RED_APPLE:
                if (len(self.snake) > 1):
                    self.process_move(next_tile_coords, 2)
                    self.gen_apples(1, Cell.RED_APPLE)
                    self.result = Movres.BAD_APPLE
                else:
                    self.process_move(next_tile_coords, 1)
                    self.gen_apples(1, Cell.RED_APPLE)
                    self.result = Movres.DEAD

    def run_action(self, action):
        match action:
            case Movdir.UP:
                self.move_checker(1, -1)
            case Movdir.LEFT:
                self.move_checker(0, -1)
            case Movdir.DOWN:
                self.move_checker(1, 1)
            case Movdir.RIGHT:
                self.move_checker(0, 1)

    def just_print_all(self):
        for y in range(self.size):
            for x in range(self.size):
                print(symbolize_cell(self.board[x + y*self.size]), end="")
            print()

    def print_a_vision(self):
        my_head = self.snake[0]
        for y in range(self.size):
            for x in range(self.size):
                if (x != my_head[0] and y != my_head[1]):
                    print(" ", end="")
                else:
                    print(
                        symbolize_cell(
                            self.board[x + y*self.size], False
                        ),
                        end=""
                    )
            print()


if (__name__ == "__main__"):
    game = Game()
    game.just_print_all()
    game.print_a_vision()
