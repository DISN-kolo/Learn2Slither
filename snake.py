#!venv/bin/python
import math
import numpy as np
from game import Game
from gui import Gui
from observer import Observer
from qtable import Qtable
from agent import Agent
from utils.mov_res import Movres


if (__name__ == "__main__"):
    print("hello snake")
    iterations = 1000
    i = 0
    training_mode = True
    naivete = False
    game = Game()
    gui = Gui(game)
    observer = Observer()
    agent = Agent()
    state = observer.observe(game, naivete)
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
    try:
        while (i < iterations):
            if (not gui.tick(game)):
                break
            action = agent.suggest_action(eps, state, qtable)
            act_result = game.run_action(action)
            reward = observer.choose_reward(act_result)
            state = observer.observe(game, naivete)
            if (training_mode):
                qslice = qtable.get_slice(state)
                old_qslice[action.value] = (
                    (1 - alpha)*old_qslice[action.value]
                    + alpha*(reward + gamma * np.max(qslice))
                )
                old_qslice = qslice
            if (act_result == Movres.WON or act_result == Movres.DEAD):
                gui.tick(game)
                break
            i += 1
            eps *= math.pow(1 - eps_reductor, i)
    finally:
        gui.close()
