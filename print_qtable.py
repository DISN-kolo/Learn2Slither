#!.venv/bin/python
import argparse
import pickle


def parse_args():
    parser = argparse.ArgumentParser(
        description="print a pickled qtable's naivety, state count and "
                     "coefficients",
    )
    parser.add_argument(
        "paths", nargs="+",
        help="paths to saved qtable models"
    )
    return parser.parse_args()


if (__name__ == "__main__"):
    args = parse_args()
    for path in args.paths:
        with open(path, "rb") as qtable_file:
            qtable = pickle.load(qtable_file)
        print("==========================================")
        print("file:", path)
        print("naivety:", qtable.naivety.name)
        print("states:", len(qtable.table))
        print("alpha:", qtable.alpha)
        print("rewards:")
        for movres, reward in qtable.rewards.items():
            print(f"  {movres.name}: {reward}")
