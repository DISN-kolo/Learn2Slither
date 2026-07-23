#!venv/bin/python
import math
import numpy as np
from game import Game
from observer import Observer
from qtable import Qtable
from agent import Agent


if (__name__ == "__main__"):
    print("hello snake")
    iterations = 1000
    i = 0
    training_mode = True
    game = Game()
    observer = Observer()
    agent = Agent()
    state = observer.observe(game)
    qtable = Qtable()
    qslice = qtable.get_slice(state)
    old_qslice = qslice
    # random-over-q preference coeff
    eps = 1.0
    eps_reductor = 0.001
    # learning coeff
    alpha = 0.9
    # discount factor
    gamma = 0.9
    while (i < iterations):
        action = agent.suggest_action(eps, state, qtable)
        #  I'm sorry, it just makes no sense to drag it out to be separately
        # processed by the observer.
        reward = game.run_action(action)
        state = observer.observe(game)
        if (training_mode):
            qslice = qtable.get_slice(state)
            old_qslice[action] = (
                (1 - alpha)*old_qslice[action]
                + alpha*(reward + gamma * np.max(qslice))
            )
            old_qslice = qslice
        i += 1
        eps *= math.pow(1 - eps_reductor, i)
