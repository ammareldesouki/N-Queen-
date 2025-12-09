# launcher.py
# GUI launcher which imports either functional.py or imperative.py and displays solutions.
# Single-file GUI (tkinter). Buttons: Previous, Next, Reset. Fixed 8x8 board.
# Aesthetics: window bg beige, board squares alternating brown/beige, queen red.

import tkinter as tk
from tkinter import ttk, messagebox
import importlib
import sys

# Default module names
MODS = {
    "Functional": "functional",
    "Imperative": "imperative"
}

# Attempt to import both solvers; will raise helpful message if missing.
for m in MODS.values():
    if m not in sys.modules:
        try:
            importlib.import_module(m)
        except Exception as e:
            # It's okay — we'll show error later when user tries to run that mode.
            pass

BOARD_SIZE = 8
CELL = 60
MARGIN = 20
CANVAS_SIZE = BOARD_SIZE * CELL + MARGIN * 2

BG_BEIGE = "#F5F0E1"
BROWN = "#A56B46"
LIGHT = "#EAD7C0"
QUEEN_RED = "#D72638"

class NQueensApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("N-Queens — 8x8")
        self.configure(bg=BG_BEIGE)
        self.resizable(False, False)

        # top controls
        frm = tk.Frame(self, bg=BG_BEIGE)
        frm.pack(padx=10, pady=10)

        tk.Label(frm, text="Choose method:", bg=BG_BEIGE).grid(row=0, column=0, sticky="w")
        self.method_var = tk.StringVar(value="Functional")
        opts = ttk.Combobox(frm, values=list(MODS.keys()), state="readonly", textvariable=self.method_var, width=12)
        opts.grid(row=0, column=1, padx=6)
        opts.bind("<<ComboboxSelected>>", lambda e: self.load_solutions())

        self.prev_btn = tk.Button(frm, text="Previous", command=self.prev_solution, width=10)
        self.prev_btn.grid(row=0, column=2, padx=6)
        self.next_btn = tk.Button(frm, text="Next", command=self.next_solution, width=10)
        self.next_btn.grid(row=0, column=3, padx=6)
        self.reset_btn = tk.Button(frm, text="Reset", command=self.reset_board, width=10)
        self.reset_btn.grid(row=0, column=4, padx=6)

        self.info_label = tk.Label(frm, text="", bg=BG_BEIGE)
        self.info_label.grid(row=1, column=0, columnspan=5, pady=(6,0))

        # canvas
        self.canvas = tk.Canvas(self, width=CANVAS_SIZE, height=CANVAS_SIZE, bg=BG_BEIGE, highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)
        self.solutions = []
        self.index = -1  # no solution shown
        self.queen_items = []

        self.draw_empty_board()

    def draw_empty_board(self):
        self.canvas.delete("all")
        # draw board background rectangle (light brown frame)
        self.canvas.create_rectangle(0,0,CANVAS_SIZE,CANVAS_SIZE, fill=BG_BEIGE, outline=BG_BEIGE)
        board_x0 = MARGIN
        board_y0 = MARGIN
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                x0 = board_x0 + c*CELL
                y0 = board_y0 + r*CELL
                x1 = x0 + CELL
                y1 = y0 + CELL
                color = BROWN if (r+c)%2==0 else LIGHT
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
        # grid lines optional (thin)
        self.canvas.create_rectangle(board_x0, board_y0,
                                     board_x0+BOARD_SIZE*CELL, board_y0+BOARD_SIZE*CELL, width=2)

    def load_solutions(self):
        method = self.method_var.get()
        module_name = MODS.get(method)
        try:
            mod = importlib.import_module(module_name)
        except Exception as e:
            messagebox.showerror("Module error", f"Can't import {module_name}. Make sure {module_name}.py is present.\n{e}")
            self.solutions = []
            self.index = -1
            self.update_info()
            return

        # call appropriate function name depending on module
        if module_name == "functional":
            sols = mod.get_solutions()
        else:
            # imperative
            sols = mod.solve_imperative()
        self.solutions = sols
        if len(self.solutions) == 0:
            self.index = -1
        else:
            self.index = 0
        self.show_current_solution()
        self.update_info()

    def update_info(self):
        total = len(self.solutions)
        idx = (self.index+1) if (0 <= self.index < total) else 0
        self.info_label.config(text=f"Method: {self.method_var.get()}  —  Solution {idx}/{total}")

    def show_current_solution(self):
        self.draw_empty_board()
        # remove any queen items
        for it in self.queen_items:
            self.canvas.delete(it)
        self.queen_items.clear()
        if not (0 <= self.index < len(self.solutions)):
            return
        sol = self.solutions[self.index]
        board_x0 = MARGIN
        board_y0 = MARGIN
        radius = CELL * 0.35
        for r, c in enumerate(sol):
            cx = board_x0 + c*CELL + CELL/2
            cy = board_y0 + r*CELL + CELL/2
            # draw a red circle as queen base and a small crown-like rectangle
            oval = self.canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, fill=QUEEN_RED, outline="")
            crown = self.canvas.create_text(cx, cy, text="♛", fill="white", font=("Arial", int(CELL*0.45)))
            self.queen_items.extend([oval, crown])
        self.update_info()

    def next_solution(self):
        if not self.solutions:
            return
        self.index = (self.index + 1) % len(self.solutions)
        self.show_current_solution()

    def prev_solution(self):
        if not self.solutions:
            return
        self.index = (self.index - 1) % len(self.solutions)
        self.show_current_solution()

    def reset_board(self):
        # Only clears queens visually but board stays visible (no queens)
        self.index = -1
        for it in self.queen_items:
            self.canvas.delete(it)
        self.queen_items.clear()
        self.update_info()


if __name__ == "__main__":
    app = NQueensApp()
    app.mainloop()
