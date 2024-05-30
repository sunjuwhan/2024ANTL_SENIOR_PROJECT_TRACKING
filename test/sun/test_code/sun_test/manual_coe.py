#!/usr/bin/env python3

"""
This example shows how to use the manual controls plugin.

Note: Manual inputs are taken from a test set in this example to decrease
complexity. Manual inputs can be received from devices such as a joystick
using third-party python extensions.

Note: Taking off the drone is not necessary before enabling manual inputs.
It is acceptable to send positive throttle input to leave the ground.
Takeoff is used in this example to decrease complexity
"""

import asyncio
import random
from mavsdk import System
from threading import*
import socket
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(("192.168.50.63",65433))

# Test set of manual inputs. Format: [roll, pitch, throttle, yaw]
manual_inputs = [
    [0, 0, 0.5, 0],  # no movement
    [-1, 0, 0.5, 0],  # minimum roll
    [1, 0, 0.5, 0],  # maximum roll
    [0, -1, 0.5, 0],  # minimum pitch
    [0, 1, 0.5, 0],  # maximum pitch
    [0, 0, 0.5, -1],  # minimum yaw
    [0, 0, 0.5, 1],  # maximum yaw
    [0, 0, 1, 0],  # max throttle
    [0, 0, 0, 0],  # minimum throttle
]


async def manual_controls():
    """Main function to connect to the drone and input manual controls"""
    # Connect to the Simulation
    drone = System()
    #await drone.connect(system_address="udp://:14540")
    await drone.connect(system_address="serial:///dev/ttyAMA0")
    # This waits till a mavlink based drone is connected
    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    # Checking if Global Position Estimate is ok
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position state is good enough for flying.")
            break

    # set the manual control input after arming
    await drone.manual_control.set_manual_control_input(
        float(0), float(0), float(0.5), float(0)
    )

    # Arming the drone
    print("-- Arming")
    await drone.action.arm()

    # Takeoff the vehicle
    print("-- Taking off")
    await drone.action.takeoff()
    await asyncio.sleep(5)

    # set the manual control input after arming
    await drone.manual_control.set_manual_control_input(
        float(0), float(0), float(0.5), float(0)
    )

    # start manual control
    #print("-- Starting manual control")
    #await drone.manual_control.start_position_control()
    print("-- Starting manual control")
    await drone.manual_control.start_position_control()
    c=0
    while True:
        try:
            c+=1
            # data=sock.recv(300).decode()
            # data=data.split(" ")
            # print(data)
            # yaw=float(data[0])
            # throttle=float(data[1])
            # roll=float(data[2])
            # pitch=float(data[3])
            await drone.manual_control.set_manual_control_input(0.0, 0.0, 0.0, 0.0)
            await asyncio.sleep(0.1)
            print(c)
            if(c==300):
                break
        except:
            continue
     
    await drone.manual_control.set_manual_control_input(0.0, 0.0, 0.5, 0.0)
    await asyncio.sleep(0.1)


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(manual_controls())