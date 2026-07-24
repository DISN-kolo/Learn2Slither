#!venv/bin/python
import math
import pickle
import time
import numpy as np
from game import Game
from gui import Gui
from observer import Observer
from qtable import Qtable
from agent import Agent
from utils.mov_res import Movres


if (__name__ == "__main__"):
    print("hello snake")
    qtable = Qtable()
    meta_iterations = 100000
    gui_after_runs = int(9*meta_iterations/10)
    gui = None
    try:
        for j in range(meta_iterations):
            training_mode = True
            naivete = False
            game = Game()
            if (gui is None and j >= gui_after_runs):
                gui = Gui(game)
            observer = Observer()
            agent = Agent()
            state = observer.observe(game, naivete)
            qslice = qtable.get_slice(state)
            old_qslice = qslice
            # random-over-q preference coeff
            eps = 1.0
            eps_reductor = 0.001
            # learning coeff
            alpha = 0.9
            # discount factor
            gamma = 0.9
            iterations = 1000
            i = 0
            while (i < iterations):
                if (gui is not None and not gui.tick(game)):
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
                    print("gg")
                    if (gui is not None):
                        gui.show_result(game, act_result == Movres.WON)
                    break
                i += 1
                eps *= math.pow(1 - eps_reductor, (i + j/10))
            print(f"session {j:10d} done after {i:7d} steps "
                f"with len {len(game.snake):10d}")
            if (gui is not None and gui.closed):
                break
    finally:
        if (gui is not None):
            gui.close()
    qtable_filename = ".qtable_finished_at." + str(int(time.time()))
    with open(qtable_filename, "wb") as qtable_file:
        pickle.dump(qtable, qtable_file)
    print(qtable)
