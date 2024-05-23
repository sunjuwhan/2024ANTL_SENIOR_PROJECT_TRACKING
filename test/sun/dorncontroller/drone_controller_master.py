import drone_controller.drone_controller_system
class class_drone_controller_master:
    def __init__(self):
        self.drone_system = drone_controller.drone_controller_system.class_Drone_Controller_System()

    def run_drone_controller(self):
        self.drone_system.run_drone_controller_system()

def main():
    obj_drone_controller_master = class_drone_controller_master()
    obj_drone_controller_master.run_drone_controller()

if __name__ == "__main__":
    main()