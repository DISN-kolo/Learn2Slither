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

The `-h` flag contains a list of helpful options. List them here or something TODO in a good way not like just the output lol
