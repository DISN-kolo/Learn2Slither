#!venv/bin/python
import argparse
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


def run_session(j, qtable, gui, training_mode, naivete):
    game = Game()
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
            print("gg")
            gui.show_result(game, act_result == Movres.WON)
            break
        i += 1
        eps *= math.pow(1 - eps_reductor, (i + j/10))
    print(f"session {j:10d} done after {i:7d} steps "
        f"with len {len(game.snake):10d}")


def run_training(qtable, meta_iterations, gui_after_runs,
                  training_mode, naivete):
    gui = Gui(Game.size, warmup_sessions=gui_after_runs)
    try:
        for j in range(meta_iterations):
            gui.begin_session(j)
            run_session(j, qtable, gui, training_mode, naivete)
            if (gui.closed):
                break
    finally:
        gui.close()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Train a snake-playing agent with Q-learning."
    )
    parser.add_argument(
        "-s", "--sessions", type=int, default=100000,
        help="number of training sessions to run (default: 100000)",
    )
    parser.add_argument(
        "-p", "--warmup-percent", type=float, default=90.0,
        help=(
            "percent of training sessions to run before the game "
            "starts being drawn (default: 90.0)"
        ),
    )
    args = parser.parse_args()
    if (args.warmup_percent < 0 or args.warmup_percent > 100):
        parser.error("--warmup-percent must be between 0 and 100")
    return args


if (__name__ == "__main__"):
    args = parse_args()
    print("hello snake")
    qtable = Qtable()
    meta_iterations = args.sessions
    gui_after_runs = int(meta_iterations * args.warmup_percent / 100)
    run_training(
        qtable, meta_iterations, gui_after_runs,
        training_mode=True, naivete=False,
    )
    qtable_filename = ".qtable_finished_at." + str(int(time.time()))
    with open(qtable_filename, "wb") as qtable_file:
        pickle.dump(qtable, qtable_file)
    print(qtable)
