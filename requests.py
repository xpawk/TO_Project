class FloorRequest:
    """Request made from a hallway call button (floor + direction)."""

    def __init__(self, floor: int, direction_up: bool):
        self.floor = floor
        self.direction_up = direction_up

class CabinRequest:
    """Request made from inside an elevator cab."""

    def __init__(self, elevator_identifier: int, floor: int):
        self.elevator_identifier = elevator_identifier
        self.floor = floor
