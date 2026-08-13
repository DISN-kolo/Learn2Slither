## Learn2Slither
42's Learn to Slither project (Q-learning a Snake game)

### Premise
Snake is a fun game. It's even more fun to leave the gameplay entirely to a soulless cold machine. This repository does exactly that: it runs an algorithm of learning to play based on remembering already-seen-before scenarios and the possible rewards obtained in them per potential action taken. For a sufficiently detailed explanation, see to [this amazing wiki article (it is literally all that's needed to understand what's happening)](https://en.wikipedia.org/wiki/Q-learning#Algorithm).

Just as a reminder - this is not considered a 'super smart' way of learning. The states here are not multidimensional, and something like

`(apple up 1, wall left 2, wall down 6, body right 1)`

is considered to be an ENTIRELY different state as compared to

`(apple up 1, wall left 2, wall down 5, body right 1)`.

The only way the model can win consistently is by learning from a huge amount of states.

(*[inspect](#model-details) the models to learn about the amount of states they have*)

### Installing
This project uses [uv](https://docs.astral.sh/uv/) to manage the Python version and dependencies.

0. install `uv` if you don't already have it (see the [uv install docs](https://docs.astral.sh/uv/getting-started/installation/))
1. for the first run, do `uv sync`

### Running
The entire program is run thru the `snake.py` file. If you've set up the venv as indicated in [Installing](#installing), then it's simply `./snake.py`, or `uv run snake.py`.

### Model details
You can find sample models in the [`/models/`](/models) subdirectory and inspect them with `uv run print_qtable.py <list of models to view>`.

By default, it performs a training run of 100k sessions with the "SMART" model selected, and the GUI starts rendering the gameplay at 90% of sessions completed. The default filename of a saved Q-table is `.qtable.<Model>.finished_at.<unix time>`.

A "SMART" model is called like that because it's not "NAIVE". A naïve model takes what the snake head sees (the entire column and the entire row) and joins it to form a state. The smart model only gets distances to the nearest non-empty object in each of the four directions. The "SMARTER" model is like the smart one but it also buckets the distances instead to keep the amount of intuitively similar but factually distinct states to a minimum. Keep in mind that it adapts to the size of the board; this *might* be considered "cheating" by some evaluators as per the subject PDF's text:

> You can only provide to the agent the information visible to your
> snake.

*Do you consider the board size to be something the snake can see immediately?* I might. In any case, the smart model does comply with the subject.

The saved Q-table contains not only the Q-table itself but also the training model; running different model types to further iterate on an already saved Q-table is impossible. This is due to models being the ways the states are remembered so changing the model mid-training would just entirely obsolete the already learned entries.

It is recommended to 'play around' with reward values as well as it can be a valuable learning experience.

### Options
Running the program with the `-h` flag will give you a list of helpful options. Here's some of the most utilized ones:

- `-S` to name the model you'll be saving after training
- `-l` to load a model
- `-T` to run with no training
- `-p` to set the % of sessions after which the GUI will start rendering the game (significant slowdown as compared to not rendering at all)
- `-n` to run with no GUI at all
- `-s` to set the amount of sessions to run for

### Licensing

See to [license](LICENSE)
