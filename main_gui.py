from tkinter import Tk
from elevator import Elevator
from building import Building
from strategy import NearestElevatorStrategy
from view_gui import ViewGUI


def create_building() -> Building:
    total_floors = 6
    elevators = [Elevator(1, 0, total_floors - 1),
                 Elevator(2, 0, total_floors - 1)]
    return Building(total_floors, elevators, NearestElevatorStrategy())


if __name__ == "__main__":
    bld = create_building()
    root = Tk()
    root.title("Mini-Elevator Simulator")
    ViewGUI(root, bld)
    root.mainloop()
