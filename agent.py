#!venv/bin/python
import random
from utils.mov_dirs import Movdir


class Agent:
    """
    Agent that can decide how to move,
    and also to put rewards into the Q table?
    Gets state from observer, but also gets the game field to act on it.
    Must never use game field info for actions.
    """

    #  choose mov dir based on state and current Q table, send it to
    # the game field. epsilon determines whether to act randomly
    # or based upon the Q table.
    def suggest_action(self, eps, state, qtable):
        qslice = qtable.get_slice(state)
        print(qslice)
        local_rand_value = random.random()
        mov_dir = -1
        if (local_rand_value > eps):
            #  pick a direction according to the qslice.
            #  since some directions may be equally max-valued,
            # pick at random between all max-valued directions.
            # TODO
            return mov_dir
        else:
            # pick a random direction.
            # up, left, down, right = 0, 1, 2, 3
            mov_dir = Movdir(random.randrange(4))
        return mov_dir
