class FloorRequest:
    """Represents a hallway call: floor + desired direction."""

    def __init__(self, floor: int, direction_up: bool):
        self.floor = floor
        self.direction_up = direction_up

    # Helpful for debugging / printing
    def __repr__(self) -> str:
        arrow = "↑" if self.direction_up else "↓"
        return f"FloorRequest({self.floor}{arrow})"


class CabinRequest:
    """Represents a button press inside a specific elevator cab."""

    def __init__(self, elevator_identifier: int, floor: int):
        self.elevator_identifier = elevator_identifier
        self.floor = floor

    def __repr__(self) -> str:
        return f"CabinRequest(E{self.elevator_identifier}→{self.floor})"
