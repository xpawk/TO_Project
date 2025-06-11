from abc import ABC, abstractmethod
from typing import List
from elevator import Elevator
from requests import FloorRequest


class DispatchStrategy(ABC):
    """Interface for elevator dispatch algorithms."""

    @abstractmethod
    def select_elevator(self, elevators: List[Elevator], request: FloorRequest) -> Elevator:  # noqa: D401,E501
        """Return the chosen elevator for the given hallway request."""
        raise NotImplementedError


class NearestElevatorStrategy(DispatchStrategy):
    """Pick the elevator whose cab is geographically closest to the request."""

    def select_elevator(self, elevators: List[Elevator], request: FloorRequest) -> Elevator:
        # Sort by (distance, current queue length, identifier) to keep output deterministic
        return min(
            elevators,
            key=lambda e: (
                abs(e.current_floor - request.floor),  # primary: absolute distance
                len(e.target_floors),                  # secondary: shorter queue is preferable
                e.identifier,                          # tertiary: deterministic tie‑break
            ),
        )


class LeastBusyElevatorStrategy(DispatchStrategy):
    """Pick the elevator with the fewest pending target floors."""

    def select_elevator(self, elevators: List[Elevator], request: FloorRequest) -> Elevator:
        # Sort by (queue length, distance, identifier) – different priority order
        return min(
            elevators,
            key=lambda e: (
                len(e.target_floors),                  # primary: minimal load
                abs(e.current_floor - request.floor),  # secondary: closer cab is nicer
                e.identifier,                          # tertiary: deterministic tie‑break
            ),
        )
