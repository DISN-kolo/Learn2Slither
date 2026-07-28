#!venv/bin/python
import argparse
import math
import os
import pickle
import time
import numpy as np
from game import Game
from gui import Gui, NullGui
from observer import Observer
from qtable import Qtable
from agent import Agent
from utils.mov_res import Movres


def run_session(
        j,
        qtable,
        gui,
        training_mode,
        naivete,
        show_field,
        show_vision,
        show_state,
        show_action,
        meta_iterations):
    game = Game()
    observer = Observer()
    agent = Agent()
    state = observer.observe(game, naivete)
    qslice = qtable.get_slice(state)
    old_qslice = qslice
    # random-over-q preference coeff
    eps = 1.0
    eps_reductor = 0.001
    #  default was for 100k, now with scaling enabled - make sure eps
    # reduction scales as well
    eps_decay_reference_sessions = 100000
    session_progress = j / meta_iterations * eps_decay_reference_sessions
    # learning coeff
    alpha = 0.9
    # discount factor
    gamma = 0.9
    iterations = 1000
    i = 0
    while (i < iterations):
        if (not gui.tick(game)):
            break
        if (show_field):
            game.just_print_all(numeric_empty=True)
        if (show_vision):
            game.print_a_vision()
        if (show_state):
            print(state)
        action = agent.suggest_action(eps, state, qtable)
        if (show_action):
            print(action.name)
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
        eps *= math.pow(1 - eps_reductor, (i + session_progress/10))
    print(f"session {j:10d} done after {i:7d} steps "
          f"with len {len(game.snake):10d}")


def run_training(
        qtable,
        meta_iterations,
        gui_after_runs,
        training_mode,
        naivete,
        show_field,
        show_vision,
        show_state,
        show_action,
        no_gui,
        auto_pause):
    if (no_gui):
        gui = NullGui()
    else:
        if (training_mode):
            warmup_text = "training..."
        else:
            warmup_text = "skipping..."
        gui = Gui(
            Game.size, warmup_sessions=gui_after_runs, auto_pause=auto_pause,
            show_skip_button=not training_mode, warmup_text=warmup_text,
        )
    try:
        for j in range(meta_iterations):
            gui.begin_session(j)
            run_session(
                j, qtable, gui, training_mode, naivete,
                show_field, show_vision, show_state, show_action,
                meta_iterations,
            )
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
    parser.add_argument(
        "-f", "--show-field", action="store_true",
        help="print the entire field on every move "
             "(W=wall, 0=empty, H=head, S=body, R=red apple, G=green apple)",
    )
    parser.add_argument(
        "-c", "--show-vision", action="store_true",
        help="print the cross-shaped view the snake sees on every move",
    )
    parser.add_argument(
        "-t", "--show-state", action="store_true",
        help="print the state tuple passed to the qtable on every move",
    )
    parser.add_argument(
        "-a", "--show-action", action="store_true",
        help="print the action taken by the agent on every move",
    )
    parser.add_argument(
        "-n", "--no-gui", action="store_true",
        help="run headless, without opening the tkinter game window "
             "(the gui is shown by default)",
    )
    parser.add_argument(
        "--auto-pause", action="store_true",
        help="pause the gui as soon as it starts rendering after the "
             "warmup sessions, instead of playing right away (off by "
             "default)",
    )
    parser.add_argument(
        "--naive", action="store_true",
        help="use naive (raw grid slice) observations instead of the "
             "nearest-object-distance ones (off by default)",
    )
    parser.add_argument(
        "--no-train", action="store_true",
        help="don't update the qtable while playing, just play with a "
             "frozen qtable (training is on by default)",
    )
    parser.add_argument(
        "--load-model", metavar="PATH", default=None,
        help="load a previously saved qtable from PATH instead of "
             "starting from an empty one (assumes it was trained "
             "with --naive off)",
    )
    parser.add_argument(
        "--save-model", metavar="PATH", default=None,
        help="save the trained qtable to PATH instead of the default "
             ".qtable_finished_at.<timestamp> filename",
    )
    args = parser.parse_args()
    if (args.warmup_percent < 0 or args.warmup_percent > 100):
        parser.error("--warmup-percent must be between 0 and 100")
    if (args.load_model and args.save_model
            and os.path.abspath(args.load_model)
            == os.path.abspath(args.save_model)):
        parser.error("--save-model must not be the same file as --load-model")
    if (args.no_train and args.save_model):
        parser.error("--save-model cannot be used with --no-train")
    return args


if (__name__ == "__main__"):
    args = parse_args()
    print("hello snake")
    if (args.load_model):
        with open(args.load_model, "rb") as qtable_file:
            qtable = pickle.load(qtable_file)
    else:
        qtable = Qtable()
    meta_iterations = args.sessions
    gui_after_runs = int(meta_iterations * args.warmup_percent / 100)
    run_training(
        qtable, meta_iterations, gui_after_runs,
        training_mode=not args.no_train, naivete=args.naive,
        show_field=args.show_field, show_vision=args.show_vision,
        show_state=args.show_state, show_action=args.show_action,
        no_gui=args.no_gui, auto_pause=args.auto_pause,
    )
    if (not args.no_train):
        if (args.save_model):
            qtable_filename = args.save_model
        else:
            qtable_filename = ".qtable_finished_at." + str(int(time.time()))
        with open(qtable_filename, "wb") as qtable_file:
            pickle.dump(qtable, qtable_file)
    print(qtable)
