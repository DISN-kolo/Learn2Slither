#!venv/bin/python
import time
import tkinter as tk
from utils.cell_types import Cell

CELL_SIZE = 30

CELL_COLORS = {
    Cell.EMPTY: "#f0f0f0",
    Cell.WALL: "#999999",
    Cell.HEAD: "#0000ff",
    Cell.BODY: "#4d79ff",
    Cell.GREEN_APPLE: "#00b300",
    Cell.RED_APPLE: "#e60000",
}


class Gui:
    """
    minimal tkinter board viewer for a running game. owns all pacing
    logic (speed slider, pause/play, single-step) so the caller's while
    loop only has to call tick(game) once per iteration and check its
    return value to know when to stop.
    """

    def __init__(self, game):
        self.root = tk.Tk()
        self.root.title("Snake Game")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self.closed = False
        self.paused = True
        self.step_requested = False
        self.delay_ms = tk.IntVar(value=150)

        board_px = game.size * CELL_SIZE
        self.canvas = tk.Canvas(
            self.root, width=board_px, height=board_px, bg="#f0f0f0"
        )
        self.canvas.pack()
        self.cell_ids = [
            [None for _ in range(game.size)] for _ in range(game.size)
        ]
        self._build_grid(game)
        self._build_controls()
        self._pump()

    def _build_grid(self, game):
        for y in range(game.size):
            for x in range(game.size):
                cell = game.board[x + y * game.size]
                cell_id = self.canvas.create_rectangle(
                    x * CELL_SIZE, y * CELL_SIZE,
                    (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                    fill=CELL_COLORS[cell], outline="black"
                )
                self.cell_ids[y][x] = cell_id

    def _build_controls(self):
        controls = tk.Frame(self.root)
        controls.pack(fill="x")

        self.play_button = tk.Button(
            controls, text="Pause", command=self._toggle_pause
        )
        self.play_button.pack(side="left", padx=4, pady=4)

        self.step_button = tk.Button(
            controls, text="Step", command=self._request_step
        )
        self.step_button.pack(side="left", padx=4, pady=4)

        tk.Label(controls, text="Delay (ms)").pack(side="left", padx=(12, 4))
        self.speed_scale = tk.Scale(
            controls, from_=1, to=500, orient="horizontal",
            showvalue=True, variable=self.delay_ms
        )
        self.speed_scale.pack(
            side="left", fill="x", expand=True, padx=4, pady=4
        )

    def _on_close(self):
        self.closed = True

    def _toggle_pause(self):
        self.paused = not self.paused
        self.play_button.config(text="Play" if (self.paused) else "Pause")

    def _request_step(self):
        self.step_requested = True

    def _pump(self):
        self.root.update_idletasks()
        self.root.update()

    def render(self, game):
        for y in range(game.size):
            for x in range(game.size):
                cell = game.board[x + y * game.size]
                self.canvas.itemconfig(
                    self.cell_ids[y][x], fill=CELL_COLORS[cell]
                )

    def tick(self, game):
        """
        redraw the board, then block the caller for as long as the
        current controls dictate: instantly if playing, until a step
        or unpause if paused. returns False once the window has been
        closed, so the caller knows to stop its loop.
        """
        self.render(game)
        self._pump()
        if (self.closed):
            return False
        if (self.paused):
            self.step_requested = False
            while (
                self.paused
                and not self.step_requested
                and not self.closed
            ):
                self._pump()
                time.sleep(0.03)
            self.step_requested = False
        else:
            elapsed = 0.0
            target = self.delay_ms.get() / 1000.0
            while (elapsed < target and not self.closed):
                time.sleep(0.01)
                elapsed += 0.01
                self._pump()
        return not self.closed

    def close(self):
        if (not self.closed):
            self.closed = True
            self.root.destroy()
