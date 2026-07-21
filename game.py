from utils.cell_types import Cell
import math


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
