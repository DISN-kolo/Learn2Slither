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


class NullGui:
    """
    a dud gui to avoid more ifs in snake.py
    """

    def __init__(self):
        self.closed = False

    def begin_session(self, j):
        pass

    def tick(self, game):
        return not self.closed

    def show_result(self, game, won):
        return not self.closed

    def close(self):
        pass


class Gui:
    """
    minimal tkinter board viewer for a running game. controls fps as well
    """

    def __init__(
            self,
            size,
            warmup_sessions=0,
            auto_pause=False,
            show_skip_button=False,
            warmup_text="training..."):
        self.root = tk.Tk()
        self.root.title("Snake Game")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self.closed = False
        self.paused = False
        self.step_requested = False
        self.skip_requested = False
        self.delay_ms = tk.IntVar(value=1)
        self.warmup_sessions = warmup_sessions
        self.auto_pause = auto_pause
        self.warmup_text = warmup_text
        self.session = 0
        self.warmup_text_id = None

        self.board_px = size * CELL_SIZE
        self.canvas = tk.Canvas(
            self.root, width=self.board_px, height=self.board_px,
            bg="#f0f0f0"
        )
        self.canvas.pack()
        self.cell_ids = [
            [None for _ in range(size)] for _ in range(size)
        ]
        self._build_grid(size)
        self._build_controls(show_skip_button)
        if (self.warmup_sessions > 0):
            self._set_warmup_text()
        self._pump()

    def _build_grid(self, size):
        for y in range(size):
            for x in range(size):
                cell_id = self.canvas.create_rectangle(
                    x * CELL_SIZE, y * CELL_SIZE,
                    (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                    fill=CELL_COLORS[Cell.EMPTY], outline="black"
                )
                self.cell_ids[y][x] = cell_id

    def _build_controls(self, show_skip_button):
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

        if (show_skip_button):
            self.skip_button = tk.Button(
                controls, text="Next Run", command=self._request_skip
            )
            self.skip_button.pack(side="left", padx=4, pady=4)

        tk.Label(controls, text="Delay (ms)").pack(side="left", padx=(12, 4))
        self.speed_scale = tk.Scale(
            controls, from_=1, to=500, orient="horizontal",
            showvalue=True, variable=self.delay_ms
        )
        self.speed_scale.pack(
            side="left", fill="x", expand=True, padx=4, pady=4
        )

    def _set_warmup_text(self):
        cx = self.board_px / 2
        cy = self.board_px / 2
        self.warmup_text_id = self.canvas.create_text(
            cx, cy, text=self.warmup_text, font=("Helvetica", 18, "bold"),
            fill="black"
        )

    def begin_session(self, j):
        """
        starts real rendering upon getting over the warmup sessions ctr
        """
        self.session = j
        if (self.session >= self.warmup_sessions
                and self.warmup_text_id is not None):
            self.canvas.delete(self.warmup_text_id)
            self.warmup_text_id = None
            if (self.auto_pause):
                self._toggle_pause()
            self._pump()

    def _on_close(self):
        self.closed = True

    def _toggle_pause(self):
        self.paused = not self.paused
        self.play_button.config(text="Play" if (self.paused) else "Pause")

    def _request_step(self):
        self.step_requested = True

    def _request_skip(self):
        self.skip_requested = True

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
        redraw the board, block the caller.
        unblock if auto-playing, or unblock on pressing 'step'.
        returns False once the window has been closed or a run-skip
        has been requested, so the caller knows to stop its loop.
        """
        if (self.session < self.warmup_sessions):
            return not self.closed
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
                and not self.skip_requested
            ):
                self._pump()
                time.sleep(0.03)
            self.step_requested = False
        else:
            elapsed = 0.0
            target = self.delay_ms.get() / 1000.0
            while (
                elapsed < target
                and not self.closed
                and not self.skip_requested
            ):
                time.sleep(0.01)
                elapsed += 0.01
                self._pump()
        if (self.skip_requested):
            self.skip_requested = False
            return False
        return not self.closed

    def show_result(self, game, won, frames=3):
        """
        overlay a WIN/LOSS banner on the board and hold it for the given
        number of paced frames, then clear it. returns False once the window
        has been closed
        """
        if (self.session < self.warmup_sessions):
            return not self.closed
        label = "WIN" if (won) else "LOSS"
        color = "#00b300" if (won) else "#e60000"
        cx = self.board_px / 2
        cy = self.board_px / 2
        text_id = self.canvas.create_text(
            cx, cy, text=label, font=("Helvetica", 28, "bold"), fill=color
        )
        pad = 12
        x0, y0, x1, y1 = self.canvas.bbox(text_id)
        box_id = self.canvas.create_rectangle(
            x0 - pad, y0 - pad, x1 + pad, y1 + pad,
            fill="#ffffff", outline="black"
        )
        self.canvas.tag_lower(box_id, text_id)
        still_open = True
        for _ in range(frames):
            still_open = self.tick(game)
            if (not still_open):
                break
        self.canvas.delete(box_id)
        self.canvas.delete(text_id)
        return still_open

    def close(self):
        if (not self.closed):
            self.closed = True
            self.root.destroy()
