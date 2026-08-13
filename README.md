## Learn2Slither
42's Learn to Slither project (Q-learning a Snake game)

### Installing
This project uses [uv](https://docs.astral.sh/uv/) to manage the Python version and dependencies.

0. install `uv` if you don't already have it (see the [uv install docs](https://docs.astral.sh/uv/getting-started/installation/))
1. for the first run, do `uv sync`

### Running
The entire program is run thru the `snake.py` file. If you've set up the venv as indicated in [Installing](#installing), then it's simply `./snake.py`, or `uv run snake.py`.

By default, it performs a training run of 100k sessions with the "SMART" model selected, and the GUI starts rendering the gameplay at 90% of sessions completed. The default filename of a saved Q-table is `.qtable.<Model>.finished_at.<unix time>`.

The saved Q-table contains not only the Q-table itself but also the training model; running different model types to further iterate on an already saved Q-table is impossible. This is due to models being the ways the states are remembered so changing the model mid-training would just entirely obsolete the already learned entries.

It is recommended to 'play around' with reward values as well as it can be a valuable learning experience. You can find sample models in the [`/models/`](/models) subdirectory and inspect them with `uv run print_qtable.py`.

Running the program with the  `-h` flag will give you a list of helpful options. Here's some of the most utilized ones:

- `-S` to name the model you'll be saving after training
- `-l` to load a model
- `-T` to run with no training
- `-p` to set the % of sessions after which the GUI will start rendering the game (significant slowdown as compared to not rendering at all)
- `-n` to run with no GUI at all
- `-s` to set the amount of sessions to run for

### Licensing

See to [license](LICENSE)
