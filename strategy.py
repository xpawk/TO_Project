from abc import ABC, abstractmethod
from typing import List

from elevator import Elevator
from requests import FloorRequest

class DispatchStrategy(ABC):
    """Interface for elevator dispatch algorithms."""

    @abstractmethod
    def select_elevator(self, elevators: List[Elevator], request: FloorRequest) -> Elevator:
        ...

class NearestElevatorStrategy(DispatchStrategy):
    """Pick the elevator whose cab is geographically closest to the request."""

    def select_elevator(self, elevators: List[Elevator], request: FloorRequest) -> Elevator:
        ...

class LeastBusyElevatorStrategy(DispatchStrategy):
    """Pick the elevator with the fewest pending target floors."""

    def select_elevator(self, elevators: List[Elevator], request: FloorRequest) -> Elevator:
        ...
