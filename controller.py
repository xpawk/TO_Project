from building import Building
from requests import FloorRequest, CabinRequest
from strategy import NearestElevatorStrategy, LeastBusyElevatorStrategy

class Controller:
    """Simple CLI controller that translates user commands into model actions."""

    HELP_TEXT = (
        "commands:\n"
        "  fr FLOOR up|down         hallway call\n"
        "  cr ELEV_ID FLOOR         cabin button press\n"
        "  strategy nearest|leastbusy  switch dispatch algorithm\n"
        "  tick                      advance simulation by one step\n"
        "  status                    dump current state\n"
        "  help                      show this help\n"
    )

    def __init__(self, building: Building):
        self.building = building

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------
    def process_user_input(self, raw: str) -> None:
        parts = raw.strip().split()
        if not parts:
            return

        cmd = parts[0].lower()

        # ------------------------------------------------ hallway calls
        if cmd == "fr" and len(parts) == 3:
            floor = self._to_int(parts[1])
            direction = parts[2].lower()
            if floor is not None and direction in {"up", "down"}:
                self.building.add_floor_request(FloorRequest(floor, direction == "up"))
            else:
                print(self.HELP_TEXT)

        # ------------------------------------------------ cabin calls
        elif cmd == "cr" and len(parts) == 3:
            elev_id = self._to_int(parts[1])
            floor = self._to_int(parts[2])
            if elev_id is not None and floor is not None:
                self.building.add_cabin_request(CabinRequest(elev_id, floor))
            else:
                print(self.HELP_TEXT)

        # ------------------------------------------------ strategy switch
        elif cmd == "strategy" and len(parts) == 2:
            name = parts[1].lower()
            if name == "nearest":
                self.building.set_dispatch_strategy(NearestElevatorStrategy())
            elif name == "leastbusy":
                self.building.set_dispatch_strategy(LeastBusyElevatorStrategy())
            else:
                print("available strategies: nearest | leastbusy")

        # ------------------------------------------------ tick / status
        elif cmd == "tick":
            self.building.step()
        elif cmd == "status":
            self.building._notify_observers() # run a tick so the view prints fresh data

        # ------------------------------------------------ help / unknown
        elif cmd in {"help", "h", "?"}:
            print(self.HELP_TEXT)
        else:
            print(self.HELP_TEXT)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _to_int(token: str):
        """Return int(token) or None if conversion fails."""
        try:
            return int(token)
        except ValueError:
            return None
