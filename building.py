from collections import deque
from typing import List, Deque, Callable

from elevator import Elevator
from requests import FloorRequest, CabinRequest
from strategy import DispatchStrategy

class Building:
    """Central model holding elevators and pending requests."""

    def __init__(self, total_floors: int, elevators: List[Elevator], dispatch_strategy: DispatchStrategy):
        self.total_floors = total_floors
        self.elevators = elevators
        self.dispatch_strategy = dispatch_strategy
        self.pending_requests: Deque[FloorRequest] = deque()
        self.observers: List[Callable[["Building"], None]] = []

    # ---- Observer helpers -------------------------------------------------
    def add_observer(self, callback):
        self.observers.append(callback)

    def notify_observers(self):
        for cb in self.observers:
            cb(self)

    # ---- API for external actors ------------------------------------------
    def add_floor_request(self, request: FloorRequest):
        ...

    def add_cabin_request(self, request: CabinRequest):
        ...

    def step(self):
        """Advance simulation by one tick and notify observers."""
        ...

    def set_dispatch_strategy(self, strategy: DispatchStrategy):
        self.dispatch_strategy = strategy
