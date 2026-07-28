#!venv/bin/python
import argparse
import matplotlib.pyplot as plt
import csv
import numpy as np

RAW_COLOR = "#112255"
MA5_COLOR = "#0099dd"
MA20_COLOR = "#ff9955"
MA150_COLOR = "#eeff00"
INK_PRIMARY = "#0b0b0b"
INK_MUTED = "#898781"
GRID_COLOR = "#e1e0d9"
SURFACE_COLOR = "#fcfcfb"


def save_stats(path, rows):
    with open(path, "w", newline="") as stats_file:
        writer = csv.writer(stats_file)
        writer.writerow(["attempt", "turns", "length"])
        writer.writerows(rows)


def load_stats(path):
    rows = []
    with open(path, newline="") as stats_file:
        reader = csv.reader(stats_file)
        next(reader)
        for row in reader:
            rows.append((int(row[0]), int(row[1]), int(row[2])))
    return rows


def moving_average(values, window):
    if (len(values) < window):
        return np.array([])
    kernel = np.ones(window) / window
    return np.convolve(values, kernel, mode="valid")


def _plot_series(ax, turns, lengths, attempts, window, color, label):
    turns_ma = moving_average(turns, window)
    lengths_ma = moving_average(lengths, window)
    attempts_ma = moving_average(attempts, window)
    if (turns_ma.size == 0):
        return
    ax.plot(
        turns_ma, lengths_ma, attempts_ma, color=color, linewidth=2,
        label=label
    )


def plot_trajectory(rows):
    if (not rows):
        return
    attempts = np.array([row[0] for row in rows], dtype=float)
    turns = np.array([row[1] for row in rows], dtype=float)
    lengths = np.array([row[2] for row in rows], dtype=float)

    fig = plt.figure(figsize=(9, 7), facecolor=SURFACE_COLOR)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor(SURFACE_COLOR)

    ax.plot(
        turns, lengths, attempts, color=RAW_COLOR, linewidth=1,
        alpha=0.35, marker="o", markersize=4, label="raw"
    )
    _plot_series(
        ax, turns, lengths, attempts, 5, MA5_COLOR, "moving avg (5)"
    )
    _plot_series(
        ax, turns, lengths, attempts, 20, MA20_COLOR, "moving avg (20)"
    )
    _plot_series(
        ax, turns, lengths, attempts, 150, MA150_COLOR, "moving avg (150)"
    )

    ax.set_xlabel("turns taken", color=INK_PRIMARY)
    ax.set_ylabel("length achieved", color=INK_PRIMARY)
    ax.set_zlabel("attempt", color=INK_PRIMARY)
    ax.set_title(
        f"training trajectory over {len(rows)} attempts",
        color=INK_PRIMARY
    )
    ax.tick_params(colors=INK_MUTED)
    ax.grid(True, color=GRID_COLOR, linewidth=0.5)
    ax.legend(frameon=False, labelcolor=INK_PRIMARY)

    fig.tight_layout()
    plt.show()


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Plot a training-stats csv file saved by "
            "snake.py --save-stats."
        )
    )
    parser.add_argument(
        "stats_file", metavar="PATH",
        help="csv file with attempt, turns, length columns",
    )
    return parser.parse_args()


if (__name__ == "__main__"):
    args = parse_args()
    plot_trajectory(load_stats(args.stats_file))
