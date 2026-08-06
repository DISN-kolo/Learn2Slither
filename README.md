## Learn2Slither
42's Learn to Slither project (Q-learning a Snake game)

### Installing
This project uses [uv](https://docs.astral.sh/uv/) to manage the Python version and dependencies.
0. install `uv` if you don't already have it (see the [uv install docs](https://docs.astral.sh/uv/getting-started/installation/))
1. for the first run, do `uv sync`

### Running
The entire program is run thru the `snake.py` file. If you've set up the venv as indicated in [Installing](#installing), then it's simply `./snake.py`, or `uv run snake.py`.

By default, it performs a training run of 100k sessions with the "SMART" model selected, and the gui starts rendering the gameplay at 90% of sessions completed. The default filename of a saved qtable is `.qtable.<Model>.finished_at.<unix time>`.

The saved qtable contains not only the qtable but also the training model; running different model types to further iterate on an already saved qtable is impossible. This is due to models being the ways the states are remembered, so changing the model mid-training would just entirely obsolete the already learned entries.

The `-h` flag contains a list of helpful options. Here's a quick look at them:

```
  -s, --sessions SESSIONS
                        number of training sessions to run (default: 100000)
  -p, --warmup-percent WARMUP_PERCENT
                        percent of training sessions to run before the game starts being
                        drawn (default: 90.0)
  -d, --dimension DIMENSION
                        board dimension, NxN playable cells (default: 10)
  -i, --iterations ITERATIONS
                        maximum number of steps allowed in a single training session
                        (default: 1000)
  -f, --show-field      print the entire field on every move (W=wall, 0=empty, H=head,
                        S=body, R=red apple, G=green apple)
  -H, --show-human-field
                        like --show-field, but empty cells are printed as spaces instead of 0
  -c, --show-vision     print the cross-shaped view the snake sees on every move
  -t, --show-state      print the state tuple passed to the qtable on every move
  -a, --show-action     print the action taken by the agent on every move
  -L, --no-session-log  don't print each session's result line (printed by default)
  -n, --no-gui          run headless, without opening the tkinter game window (the gui is
                        shown by default)
  -P, --auto-pause      pause the gui as soon as it starts rendering after the warmup
                        sessions, instead of playing right away (off by default)
  -N, --naivety {NAIVE,SMART,SMARTER}
                        state representation to use: NAIVE (grid v/h cross - kept only to
                        show how ineffective it is, don't use), SMART (nearest-object-
                        distance, default), or SMARTERlike SMART, but bucketed: 0..1, 2..4,
                        5..7, 8..+inf). Illegal together with --load-model, since the qtable
                        object has this info written in it.
  -T, --no-train        don't train/update the qtable while playing, just play (training is
                        on by default)
  -l, --load-model PATH
                        load a previously saved qtable from PATH instead of starting from an
                        empty one; its naivety level is read from the file itself
  -S, --save-model PATH
                        save the trained qtable to PATH instead of the default
                        .qtable.<naivety>.finished_at.<timestamp> filename
  -D, --save-stats PATH
                        write per-attempt (attempt, turns, length) stats to PATH as csv
```
