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
from utils.naivety import Naivety
from stats import save_stats, plot_trajectory


def run_session(
        j,
        qtable,
        gui,
        training_mode,
        dimension,
        iterations,
        show_field,
        show_human_field,
        show_vision,
        show_state,
        show_action,
        show_session_log,
        meta_iterations):
    game = Game(dimension)
    observer = Observer()
    agent = Agent()
    state = observer.observe(game, qtable.naivety)
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
    i = 0
    while (i < iterations):
        if (not gui.tick(game, i)):
            break
        if (show_field):
            game.just_print_all(numeric_empty=True)
        if (show_human_field):
            game.just_print_all(numeric_empty=False)
        if (show_vision):
            game.print_a_vision()
        if (show_state):
            print(state)
        action = agent.suggest_action(eps, state, qtable)
        if (show_action):
            print(action.name)
        act_result = game.run_action(action)
        reward = observer.choose_reward(act_result)
        state = observer.observe(game, qtable.naivety)
        if (training_mode):
            qslice = qtable.get_slice(state)
            old_qslice[action.value] = (
                (1 - alpha)*old_qslice[action.value]
                + alpha*(reward + gamma * np.max(qslice))
            )
            old_qslice = qslice
        if (act_result == Movres.DEAD):
            gui.show_result(game, len(game.snake) >= 10, i)
            break
        i += 1
        eps *= math.pow(1 - eps_reductor, (i + session_progress/10))
    if (show_session_log):
        print(f"session {j:10d} done after {i:7d} steps "
              f"with len {len(game.snake):10d}")
    return len(game.snake), i


def run_training(
        qtable,
        meta_iterations,
        gui_after_runs,
        training_mode,
        dimension,
        iterations,
        show_field,
        show_human_field,
        show_vision,
        show_state,
        show_action,
        show_session_log,
        no_gui,
        auto_pause,
        stats_path):
    if (no_gui):
        gui = NullGui()
    else:
        if (training_mode):
            warmup_text = "training..."
        else:
            warmup_text = "skipping..."
        gui = Gui(
            dimension, iterations, meta_iterations,
            warmup_sessions=gui_after_runs, auto_pause=auto_pause,
            show_skip_button=not training_mode, warmup_text=warmup_text,
        )
    max_length = 0
    max_turns = 0
    stats_rows = []
    try:
        for j in range(meta_iterations):
            gui.begin_session(j)
            session_length, session_turns = run_session(
                j, qtable, gui, training_mode, dimension,
                iterations, show_field, show_human_field, show_vision,
                show_state, show_action, show_session_log, meta_iterations,
            )
            max_length = max(max_length, session_length)
            max_turns = max(max_turns, session_turns)
            if (stats_path):
                stats_rows.append((j, session_turns, session_length))
            if (gui.closed):
                break
    except KeyboardInterrupt:
        print("\ninterrupted, saving progress so far...")
    finally:
        gui.close()
    if (stats_path and stats_rows):
        save_stats(stats_path, stats_rows)
        plot_trajectory(stats_rows)
    return max_length, max_turns


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
        "-d", "--dimension", type=int, default=10,
        help="board dimension, NxN playable cells (default: 10)",
    )
    parser.add_argument(
        "-i", "--iterations", type=int, default=1000,
        help="maximum number of steps allowed in a single training "
             "session (default: 1000)",
    )
    parser.add_argument(
        "-f", "--show-field", action="store_true",
        help="print the entire field on every move "
             "(W=wall, 0=empty, H=head, S=body, R=red apple, G=green apple)",
    )
    parser.add_argument(
        "-H", "--show-human-field", action="store_true",
        help="like --show-field, but empty cells are printed as spaces "
             "instead of 0",
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
        "-L", "--no-session-log", action="store_true",
        help="don't print each session's result line "
             "(printed by default)",
    )
    parser.add_argument(
        "-n", "--no-gui", action="store_true",
        help="run headless, without opening the tkinter game window "
             "(the gui is shown by default)",
    )
    parser.add_argument(
        "-P", "--auto-pause", action="store_true",
        help="pause the gui as soon as it starts rendering after the "
             "warmup sessions, instead of playing right away (off by "
             "default)",
    )
    parser.add_argument(
        "-N", "--naivety", choices=[level.name for level in Naivety],
        default=None,
        help="state representation to use: NAIVE (grid v/h cross - kept "
             "only to show how ineffective it is, don't use), SMART "
             "(nearest-object-distance, default), or SMARTER"
             "like SMART, but bucketed: 0..1, 2..4, 5..8, 9..+inf). "
             "Illegal together with --load-model, "
             "since the qtable object has this info written in it.",
    )
    parser.add_argument(
        "-T", "--no-train", action="store_true",
        help="don't train/update the qtable while playing, just play "
             "(training is on by default)",
    )
    parser.add_argument(
        "-l", "--load-model", metavar="PATH", default=None,
        help="load a previously saved qtable from PATH instead of "
             "starting from an empty one; its naivety level is read "
             "from the file itself",
    )
    parser.add_argument(
        "-S", "--save-model", metavar="PATH", default=None,
        help="save the trained qtable to PATH instead of the default "
             ".qtable.<naivety>.finished_at.<timestamp> filename",
    )
    parser.add_argument(
        "-D", "--save-stats", metavar="PATH", default=None,
        help="write per-attempt (attempt, turns, length) stats to PATH "
             "as csv, and show a turns-vs-length training trajectory "
             "(with 5- and 20-attempt moving averages) in a matplotlib "
             "window once training ends",
    )
    args = parser.parse_args()
    if (args.warmup_percent < 0 or args.warmup_percent > 100):
        parser.error("--warmup-percent must be between 0.0 and 100.0")
    if (args.dimension < 5):
        parser.error("--dimension must be at least 5")
    if (args.iterations < 1):
        parser.error("--iterations must be at least 1")
    if (args.load_model and args.naivety is not None):
        parser.error("--naivety cannot be used together with "
                     "--load-model; the loaded model already carries "
                     "its own naivety level")
    if (args.naivety is None):
        args.naivety = Naivety.SMART
    else:
        args.naivety = Naivety[args.naivety]
    if (args.load_model and args.save_model
            and os.path.abspath(args.load_model)
            == os.path.abspath(args.save_model)):
        parser.error("--save-model must not be the same file as --load-model")
    if (args.no_train and args.save_model):
        parser.error("--save-model cannot be used with --no-train")
    if (args.show_field and args.show_human_field):
        parser.error("--show-field and --show-human-field are mutually "
                     "exclusive")
    return args


if (__name__ == "__main__"):
    args = parse_args()
    print("hello snake")
    if (args.load_model):
        with open(args.load_model, "rb") as qtable_file:
            qtable = pickle.load(qtable_file)
    else:
        qtable = Qtable(args.naivety)
    meta_iterations = args.sessions
    gui_after_runs = int(meta_iterations * args.warmup_percent / 100)
    max_length, max_turns = run_training(
        qtable, meta_iterations, gui_after_runs,
        training_mode=not args.no_train,
        dimension=args.dimension, iterations=args.iterations,
        show_field=args.show_field, show_human_field=args.show_human_field,
        show_vision=args.show_vision,
        show_state=args.show_state, show_action=args.show_action,
        show_session_log=not args.no_session_log,
        no_gui=args.no_gui, auto_pause=args.auto_pause,
        stats_path=args.save_stats
    )
    if (not args.no_train):
        if (args.save_model):
            qtable_filename = args.save_model
        else:
            qtable_filename = (".qtable."
                               + qtable.naivety.name
                               + ".finished_at." + str(int(time.time()))
                               )
        with open(qtable_filename, "wb") as qtable_file:
            pickle.dump(qtable, qtable_file)
    print(f"max length achieved: {max_length}")
    print(f"max turns taken: {max_turns}")
