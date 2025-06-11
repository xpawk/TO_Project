from elevator import ElevatorState
from building import Building

class ViewCLI:
    """Console view that prints the state after every simulation tick."""

    def __init__(self, building: Building) -> None:
        self._tick = 0
        building.add_observer(self.render)

    # ------------------------------------------------------------------
    # Observer callback
    # ------------------------------------------------------------------
    def render(self, building: Building) -> None:
        self._tick += 1
        print(f"\n--- tick {self._tick} ---")

        for elevator in building.elevators:
            queue = list(elevator.target_floors)
            print(
                f"E{elevator.identifier} | floor {elevator.current_floor} | "
                f"{elevator.state.name} | queue {queue}"
            )

        if building.hallway_queue:
            hall_calls = " ".join(
                f"{req.floor}{'↑' if req.direction_up else '↓'}"
                for req in building.hallway_queue
            )
            print("pending hallway calls:", hall_calls)

        print("----------------")
