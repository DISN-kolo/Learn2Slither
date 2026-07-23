from utils.cell_types import Cell


class Observer:
    # naïveté being false means doing the smart approach of observing
    #the distances to the nearest non-empty cells. the return format in
    #that case is a tuple of (Cell.TYPE, distance, ...) in the usual
    #up, left, down, right format.
    # if the naïveté parameter is true, however, just fill up the return
    #tuple with the vertical slice followed by the horizontal slice.
    def observe(self, game, naivete):
        head_of_snake = game.snake[0]
        arr = []
        if (naivete):
            for y in range(game.size):
                arr.append(game.board[head_of_snake[0] + y*game.size])
            for x in range(game.size):
                arr.append(game.board[x + head_of_snake[1]*game.size])
        else:
            # XXX boilerplate removal?
            # up
            observed_cell = Cell.EMPTY
            distance = 0
            while (observed_cell == Cell.EMPTY):
                distance += 1
                observed_cell = game.board[
                    head_of_snake[0]
                    + (head_of_snake[1] - distance)*game.size
                ]
            arr.append(observed_cell, distance)
            # left
            observed_cell = Cell.EMPTY
            distance = 0
            while (observed_cell == Cell.EMPTY):
                distance += 1
                observed_cell = game.board[
                    head_of_snake[0] - distance
                    + head_of_snake[1]*game.size
                ]
            arr.append(observed_cell, distance)
            # down
            observed_cell = Cell.EMPTY
            distance = 0
            while (observed_cell == Cell.EMPTY):
                distance += 1
                observed_cell = game.board[
                    head_of_snake[0]
                    + (head_of_snake[1] + distance)*game.size
                ]
            arr.append(observed_cell, distance)
            # right
            observed_cell = Cell.EMPTY
            distance = 0
            while (observed_cell == Cell.EMPTY):
                distance += 1
                observed_cell = game.board[
                    head_of_snake[0] + distance
                    + head_of_snake[1]*game.size
                ]
            arr.append(observed_cell, distance)
        res = tuple(arr)
        return res
