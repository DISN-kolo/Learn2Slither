#!venv/bin/python
from utils.cell_types import Cell
import random
import numpy as np


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
        res = []
        for i in range(count):
            x_pick = random.randrange(1, self.dimension + 1)
            y_pick = random.randrange(1, self.dimension + 1)
            attempts = 0
            while (self.board[x_pick + y_pick*12] != Cell.EMPTY
                    and attempts < 100):
                x_pick = random.randrange(1, self.dimension + 1)
                y_pick = random.randrange(1, self.dimension + 1)
                attempts += 1
            if (attempts >= 100):
                raise Exception("Too many apple placement attemps; "\
                    "board too crowded?")
            self.board[x_pick + y_pick*12] = kind
            res.append([x_pick, y_pick])
        return np.array(res)

    def __init__(self):
        #   x - >
        # y  0  1  2  3  4  5  6  7  8  9 10 11
        # | 12 13 14 15 16 17 18 19 20 21 22 23
        # v
        #
        # so, to get x: % 12
        # to get y: / 12
        #
        # from xy to i then:
        # i = x + y*12
        self.board = [
            Cell.EMPTY if (
                (i % self.size != 0)
                and (i % self.size != self.size - 1)
                and (i > self.size)
                and (i < self.size*(self.size - 1)))
            else Cell.WALL for i in range(12*12)]
        self.snake = np.array(generate_init_snake_coords(self.dimension)) + 1
        ctr = 0
        for xy_pair in self.snake:
            if (ctr == 0):
                self.board[xy_pair[0] + xy_pair[1]*12] = Cell.HEAD
            else:
                self.board[xy_pair[0] + xy_pair[1]*12] = Cell.BODY
            ctr += 1
        self.red_apples = self.gen_apples(1, Cell.RED_APPLE)
        self.green_apples = self.gen_apples(2, Cell.GREEN_APPLE)

    def just_print_all(self):
        for y in range(self.size):
            for x in range(self.size):
                print(symbolize_cell(self.board[x + y*12]), end="")
            print()

    def print_a_vision(self):
        my_head = self.snake[0]
        for y in range(self.size):
            for x in range(self.size):
                if (x != my_head[0] and y != my_head[1]):
                    print(" ", end="")
                else:
                    print(symbolize_cell(self.board[x + y*12], False), end="")
            print()


if (__name__ == "__main__"):
    game = Game()
    game.just_print_all()
    game.print_a_vision()
