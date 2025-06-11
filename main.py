import sys
from tkinter import Tk
from elevator import Elevator
from building import Building
from strategy import NearestElevatorStrategy
from controller import Controller
from view_cli import ViewCLI
from view_gui import ViewGUI


def create_building() -> Building:
    """Factory that returns a Building with two elevators and the default strategy."""
    total_floors = 6                                  # change if you need more
    elevators = [
        Elevator(1, 0, total_floors - 1),
        Elevator(2, 0, total_floors - 1),
    ]
    return Building(total_floors, elevators, NearestElevatorStrategy())


def run_gui(building: Building) -> None:
    """Launch the Tkinter GUI."""
    root = Tk()
    root.title("Mini-Elevator Simulator")
    ViewGUI(root, building)
    root.mainloop()


def run_cli(building: Building) -> None:
    """Start the text-based interface."""
    ViewCLI(building)                # registers itself as observer
    controller = Controller(building)
    print("CLI mode – type 'help' for commands, Ctrl+C to quit.")
    try:
        while True:
            command = input("> ")
            controller.process_user_input(command)
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    # Mode selection: 1) command-line arg, 2) interactive prompt
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    if mode not in {"gui", "cli"}:
        mode = input("Choose interface (gui/cli) [gui]: ").strip().lower() or "gui"

    building = create_building()

    if mode == "cli":
        run_cli(building)
    else:                               # default = GUI
        run_gui(building)
