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
    print(res)
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
    print("second chunk:")
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
    print("last chunk:")
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
    print(res)
    return res


class Game:
    """Describes the game field. Can act on it, can return general info"""
    dimension = 10
    size = dimension + 2

    def __init__(self):
        #   x - >
        # y  0  1  2  3  4  5  6  7  8  9 10 11
        # | 12 13 14 15 16 17 18 19 20 21 22 23
        # v
        #
        # so, to get x: % 12
        # to get y: / 12
        self.board = [
            Cell.EMPTY if (
                (i % self.size != 0)
                and (i % self.size != self.size - 1)
                and (i > self.size)
                and (i < self.size*(self.size - 1)))
            else Cell.WALL for i in range(12*12)]
        self.snake = np.array(generate_init_snake_coords(self.dimension)) + 1
        print(self.snake)


if (__name__ == "__main__"):
    game = Game()
