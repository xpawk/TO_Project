from building import Building

class ViewCLI:
    """Text‑based view that prints the current state after each tick."""

    def __init__(self, building: Building):
        self.building = building
        self.building.add_observer(self.render)

    def render(self, building: Building):
        """Render the building state to the console."""
        ...
