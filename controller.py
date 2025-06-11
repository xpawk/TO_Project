from building import Building
from requests import FloorRequest, CabinRequest
from strategy import NearestElevatorStrategy, LeastBusyElevatorStrategy

class Controller:
    """Handles user commands and updates the model accordingly."""

    def __init__(self, building: Building):
        self.building = building

    def process_user_input(self, command: str):
        """Parse CLI commands and interact with the building model."""
        ...
