from elevator import Elevator
from building import Building
from strategy import NearestElevatorStrategy
from controller import Controller
from view_cli import ViewCLI


def create_default_building() -> Building:
    total_floors = 6
    elevators = [Elevator(1, 0, total_floors - 1), Elevator(2, 0, total_floors - 1)]
    strategy = NearestElevatorStrategy()
    return Building(total_floors, elevators, strategy)


def main():
    building = create_default_building()
    ViewCLI(building)  # observer registers itself
    controller = Controller(building)

    while True:
        command = input("Enter command: ")
        controller.process_user_input(command)
        building.step()


if __name__ == "__main__":
    main()
