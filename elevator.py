from enum import Enum
from collections import deque
from typing import Deque

class ElevatorState(Enum):
    IDLE = 0
    MOVING_UP = 1
    MOVING_DOWN = 2
    DOORS_OPEN = 3

class Elevator:
    """
    Represents a single elevator cab.

    State machine:
      • IDLE – waiting for work
      • MOVING_UP / MOVING_DOWN – travelling toward first item in the queue
      • DOORS_OPEN – doors stay open for one tick, then we pop the floor from the queue
    """

    def __init__(self, identifier: int, current_floor: int, total_floors: int):
        self.identifier = identifier
        self.current_floor = current_floor
        self.total_floors = total_floors
        self.state: ElevatorState = ElevatorState.IDLE
        self.target_floors: Deque[int] = deque()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_target_floor(self, floor: int) -> None:
        """Queue a new floor (if in range and not already queued)."""
        if 0 <= floor <= self.total_floors and floor not in self.target_floors:
            self.target_floors.append(floor)

    def step(self) -> None:
        """Advance elevator state by one simulation tick."""
        if self.state == ElevatorState.IDLE:
            if self.target_floors:
                self._set_direction_towards(self.target_floors[0])
            return

        if self.state == ElevatorState.MOVING_UP:
            self.current_floor += 1
            if self.current_floor == self.target_floors[0]:
                self.state = ElevatorState.DOORS_OPEN
            return

        if self.state == ElevatorState.MOVING_DOWN:
            self.current_floor -= 1
            if self.current_floor == self.target_floors[0]:
                self.state = ElevatorState.DOORS_OPEN
            return

        if self.state == ElevatorState.DOORS_OPEN:
            # Remove the floor we just served
            if self.target_floors:
                self.target_floors.popleft()
            # Decide next action
            if self.target_floors:
                self._set_direction_towards(self.target_floors[0])
            else:
                self.state = ElevatorState.IDLE

    def is_idle(self) -> bool:
        """Return True when there is nothing to do."""
        return self.state == ElevatorState.IDLE and not self.target_floors

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _set_direction_towards(self, target: int) -> None:
        if target > self.current_floor:
            self.state = ElevatorState.MOVING_UP
        elif target < self.current_floor:
            self.state = ElevatorState.MOVING_DOWN
        else:
            self.state = ElevatorState.DOORS_OPEN
