from enum import Enum
from collections import deque
from typing import Deque

class ElevatorState(Enum):
    IDLE = 0
    MOVING_UP = 1
    MOVING_DOWN = 2
    DOORS_OPEN = 3

class Elevator:
    """Represents a single elevator cab."""

    def __init__(self, identifier: int, current_floor: int, total_floors: int):
        self.identifier = identifier
        self.current_floor = current_floor
        self.total_floors = total_floors
        self.state: ElevatorState = ElevatorState.IDLE
        self.target_floors: Deque[int] = deque()

    def add_target_floor(self, floor: int):
        """Queue a new destination floor for this elevator."""
        ...

    def step(self):
        """Advance elevator state by one simulation tick."""
        ...

    def is_idle(self) -> bool:
        """Return True if the elevator has no pending targets."""
        ...
