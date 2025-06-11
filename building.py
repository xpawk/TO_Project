from collections import deque
from typing import List, Deque, Callable

from elevator import Elevator
from requests import FloorRequest, CabinRequest
from strategy import DispatchStrategy


class Building:
    """Holds elevators and pending hallway requests; advances the simulation one tick at a time."""

    def __init__(
        self,
        total_floors: int,
        elevators: List[Elevator],
        dispatch_strategy: DispatchStrategy,
    ):
        self.total_floors = total_floors
        self.elevators = elevators
        self.dispatch_strategy = dispatch_strategy
        self.hallway_queue: Deque[FloorRequest] = deque()
        self._observers: List[Callable[["Building"], None]] = []

    # ------------------------------------------------------------------
    # Observer helpers
    # ------------------------------------------------------------------
    def add_observer(self, callback: Callable[["Building"], None]) -> None:
        self._observers.append(callback)

    def _notify_observers(self) -> None:
        for cb in self._observers:
            cb(self)

    # ------------------------------------------------------------------
    # Public API – called by the controller
    # ------------------------------------------------------------------
    def add_floor_request(self, request: FloorRequest) -> None:
        """Add a hallway call (floor + direction) to the queue."""
        self.hallway_queue.append(request)

    def add_cabin_request(self, request: CabinRequest) -> None:
        """Route a cabin button press to the appropriate elevator."""
        for elevator in self.elevators:
            if elevator.identifier == request.elevator_identifier:
                elevator.add_target_floor(request.floor)
                return
        print(f"[warning] Elevator with id {request.elevator_identifier} not found")

    def set_dispatch_strategy(self, strategy: DispatchStrategy) -> None:
        self.dispatch_strategy = strategy

    # ------------------------------------------------------------------
    # Simulation tick
    # ------------------------------------------------------------------
    def step(self) -> None:
        """Process hallway queue, move all elevators and notify observers."""
        # 1) Assign every queued hallway request to an elevator via the strategy.
        while self.hallway_queue:
            call = self.hallway_queue.popleft()
            chosen_elevator = self.dispatch_strategy.select_elevator(
                self.elevators, call
            )
            chosen_elevator.add_target_floor(call.floor)

        # 2) Advance each elevator by one tick.
        for elevator in self.elevators:
            elevator.step()

        # 3) Notify any observers (e.g. CLI view).
        self._notify_observers()
