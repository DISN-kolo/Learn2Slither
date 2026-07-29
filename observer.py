from utils.cell_types import Cell
from utils.mov_res import Movres
from utils.naivety import Naivety
from utils.distance_buckets import DistanceBucket


def choose_d_bucket(distance):
    if (distance <= 1):
        return DistanceBucket.NEXT
    if (2 <= distance <= 4):
        return DistanceBucket.CLOSE
    if (5 <= distance <= 7):
        return DistanceBucket.FAR
    else:
        return DistanceBucket.VERY_FAR


class Observer:
    #  NAIVE fills up the return tuple with the vertical slice followed
    # by the horizontal slice. pretty naïve if you ask me
    #  SMART gets the distance to the nearest non-empty cell in
    # each of the 4 directions and returns a tuple of
    # the (type, dist, type, dist...) kind
    #  SMARTER is like SMART, but gets the buckets of distances instead
    # (feels smarter, eh?)
    def observe(self, game, naivety):
        head_of_snake = game.snake[0]
        arr = []
        match naivety:
            case Naivety.NAIVE:
                for y in range(game.size):
                    arr.append(
                        game.board[head_of_snake[0] + y*game.size]
                    )
                for x in range(game.size):
                    arr.append(
                        game.board[x + head_of_snake[1]*game.size]
                    )
            case Naivety.SMART:
                # up, left, down, right = [0], [1], [2], [3]
                directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
                head_x, head_y = head_of_snake[0], head_of_snake[1]
                for dx, dy in directions:
                    if (head_x == 0 or head_x == game.size - 1
                            or head_y == 0 or head_y == game.size - 1):
                        arr.append(Cell.WALL)
                        arr.append(0)
                        continue
                    observed_cell = Cell.EMPTY
                    distance = 0
                    while (observed_cell == Cell.EMPTY):
                        distance += 1
                        x = head_x + dx*distance
                        y = head_y + dy*distance
                        if (x < 0
                                or x >= game.size
                                or y < 0
                                or y >= game.size):
                            observed_cell = Cell.WALL
                            break
                        observed_cell = game.board[x + y*game.size]
                    arr.append(observed_cell)
                    arr.append(distance)
            case Naivety.SMARTER:
                directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
                head_x, head_y = head_of_snake[0], head_of_snake[1]
                for dx, dy in directions:
                    if (head_x == 0 or head_x == game.size - 1
                            or head_y == 0 or head_y == game.size - 1):
                        arr.append(Cell.WALL)
                        arr.append(DistanceBucket.NEXT)
                        continue
                    observed_cell = Cell.EMPTY
                    distance = 0
                    while (observed_cell == Cell.EMPTY):
                        distance += 1
                        x = head_x + dx*distance
                        y = head_y + dy*distance
                        if (x < 0
                                or x >= game.size
                                or y < 0
                                or y >= game.size):
                            observed_cell = Cell.WALL
                            break
                        observed_cell = game.board[x + y*game.size]
                    arr.append(observed_cell)
                    arr.append(choose_d_bucket(distance))
                pass
        res = tuple(arr)
        return res

    def choose_reward(self, act_result):
        match act_result:
            case Movres.NORMAL:
                return -1
            case Movres.DEAD:
                return -75
            case Movres.GOOD_APPLE:
                return 10
            case Movres.BAD_APPLE:
                return -5
            case Movres.WON:
                return 15
            case Movres.EXTRA_GOOD_APPLE:
                return 20
