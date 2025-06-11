# view_gui.py – big labels, sidebar cabin panel, auto-tick
import tkinter as tk
from tkinter import ttk

from building import Building
from elevator import Elevator, ElevatorState
from requests import FloorRequest, CabinRequest
from strategy import NearestElevatorStrategy, LeastBusyElevatorStrategy

# ───────── drawing constants ─────────────────────────────────────────────
SHAFT_W = 90
MARGIN  = 6
CAB_H   = 24
CAB_W   = SHAFT_W - 2 * MARGIN
GAP     = 18
TICK_MS = 1000  # >0 → auto-tick every n ms

STRATEGIES = {
    "Nearest":    NearestElevatorStrategy,
    "Least busy": LeastBusyElevatorStrategy,
}


class ViewGUI(ttk.Frame):
    """Tkinter front-end: hallway buttons, strategy switcher, embedded cabin panel."""

    # ────────────────────────────── init ────────────────────────────────
    def __init__(self, root: tk.Tk, building: Building) -> None:
        super().__init__(root, padding=5)
        self.grid(sticky="nsew")
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        self.building = building
        self._floors  = building.total_floors         
        self._cab_tags: dict[str, Elevator] = {}
        self._selected: Elevator | None = None
        building.add_observer(self._redraw)

        self._create_left_panel()
        self._create_canvas()
        self._create_right_panel()

        self._redraw(building)
        if TICK_MS:
            self._auto_tick()

    # ───────────────────────── left panel ───────────────────────────────
    def _create_left_panel(self):
        pane = ttk.Frame(self)
        pane.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        ttk.Label(pane, text="Hall calls", font=("Segoe UI", 11, "bold")).pack()

        top_floor = self._floors - 1
        for fl in reversed(range(self._floors)):        
            row = ttk.Frame(pane)
            row.pack(fill="x")

            # “↑” only if not on top floor
            if fl < top_floor:
                ttk.Button(
                    row, text=f"{fl} ↑", width=5,
                    command=lambda f=fl: self._hall_call(f, True)
                ).pack(side="left")
            else:
                ttk.Label(row, text="     ").pack(side="left")  # spacer

            # “↓” only if not on ground floor
            if fl > 0:
                ttk.Button(
                    row, text=f"{fl} ↓", width=5,
                    command=lambda f=fl: self._hall_call(f, False)
                ).pack(side="left")

    # ───────────────────────── canvas ───────────────────────────────────
    def _create_canvas(self):
        width  = len(self.building.elevators) * SHAFT_W + 40  # room for numbers
        height = self._floors * GAP + 60                      # exact floor count
        self.canvas = tk.Canvas(self, width=width, height=height, bg="white")
        self.canvas.grid(row=0, column=1, sticky="nsew")
        self.canvas.bind("<Button-1>", self._on_canvas_click)

    # ───────────────────────── right panel  ──────────────────
    def _create_right_panel(self):
        right = ttk.Frame(self)
        right.grid(row=0, column=2, sticky="ns")

        ttk.Label(right, text="Strategy", font=("Segoe UI", 11, "bold")).pack()
        self._strategy_var = tk.StringVar(value="Nearest")
        for name in STRATEGIES:
            ttk.Radiobutton(
                right, text=name, value=name, variable=self._strategy_var,
                command=self._on_strategy_change,
            ).pack(anchor="w")

        ttk.Separator(right, orient="horizontal").pack(fill="x", pady=8)
        ttk.Button(right, text="Tick", command=self._tick).pack(fill="x")
        ttk.Button(right, text="Quit", command=self.quit).pack(fill="x", pady=6)

        ttk.Separator(right, orient="horizontal").pack(fill="x", pady=8)
        self.cabin_frame = ttk.Frame(right)
        self.cabin_frame.pack(fill="x")

    # ───────────────────────── event helpers ────────────────────────────
    def _on_strategy_change(self):
        self.building.set_dispatch_strategy(STRATEGIES[self._strategy_var.get()]())

    def _hall_call(self, floor: int, up: bool):
        self.building.add_floor_request(FloorRequest(floor, up))

    def _tick(self):
        self.building.step()

    def _auto_tick(self):
        self._tick()
        self.after(TICK_MS, self._auto_tick)

    def _on_canvas_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if not item:
            return
        tag = next((t for t in self.canvas.gettags(item) if t.startswith("cab")), None)
        if tag and tag in self._cab_tags:
            self._selected = self._cab_tags[tag]
            self._build_cabin_panel()

    # ───────────────────────── cabin panel ──────────────────────────────
    def _build_cabin_panel(self):
        for child in self.cabin_frame.winfo_children():
            child.destroy()
        if not self._selected:
            return

        elev = self._selected
        ttk.Label(
            self.cabin_frame, text=f"Cabin E{elev.identifier}",
            font=("Segoe UI", 10, "bold"), padding=2
        ).pack()

        grid = ttk.Frame(self.cabin_frame)
        grid.pack(pady=2)
        for i, fl in enumerate(reversed(range(self._floors))):
            ttk.Button(
                grid, text=str(fl), width=3,
                command=lambda f=fl, e=elev: self._cabin_call(e, f)
            ).grid(row=i // 3, column=i % 3, padx=1, pady=1)

        ttk.Button(self.cabin_frame, text="Clear", command=self._clear_selection).pack(pady=4)

    def _cabin_call(self, elevator: Elevator, floor: int):
        self.building.add_cabin_request(CabinRequest(elevator.identifier, floor))

    def _clear_selection(self):
        self._selected = None
        for child in self.cabin_frame.winfo_children():
            child.destroy()

    # ───────────────────────── drawing ──────────────────────────────────
    def _redraw(self, _: Building):
        self.canvas.delete("all")
        self._cab_tags.clear()
        self._draw_floor_lines()

        for idx, elev in enumerate(self.building.elevators):
            x0 = 40 + idx * SHAFT_W + MARGIN
            x1 = x0 + SHAFT_W - 2 * MARGIN
            y  = self._floor_to_y(elev.current_floor) - CAB_H

            self.canvas.create_rectangle(x0, 20, x1, self._canvas_h() - 20, outline="#888")

            tag = f"cab{elev.identifier}"
            colour = "#4caf50" if elev.state != ElevatorState.IDLE else "#2196f3"
            self.canvas.create_rectangle(x0 + 1, y, x0 + CAB_W, y + CAB_H,
                                         fill=colour, outline="", tags=tag)
            self.canvas.create_text(x0 + CAB_W / 2, y + CAB_H / 2,
                                    text=f"E{elev.identifier}", fill="white", tags=tag)
            self._cab_tags[tag] = elev

            arrow = {"MOVING_UP": "↑", "MOVING_DOWN": "↓"}.get(elev.state.name, "")
            self.canvas.create_text(x1 + 10, y + CAB_H / 2, text=arrow, font=("Segoe UI", 12))

            queue = list(elev.target_floors)
            if queue:
                self.canvas.create_text(
                    x0 + CAB_W / 2, y - 14,
                    text="→ " + ",".join(map(str, queue)),
                    font=("Segoe UI", 8)
                )

    def _draw_floor_lines(self):
        label_font = ("Segoe UI", 12, "bold")
        for fl in range(self._floors):                       # 0 … top-1
            y = self._floor_to_y(fl)
            self.canvas.create_line(40, y, self.canvas.winfo_width(), y, fill="#e0e0e0")
            self.canvas.create_text(20, y - 8, text=str(fl), font=label_font, anchor="e")

    # ───────────────────────── helpers ──────────────────────────────────
    def _floor_to_y(self, floor: int) -> int:
        return (self._floors - 1 - floor) * GAP + 50

    def _canvas_h(self) -> int:
        return self._floors * GAP + 60
