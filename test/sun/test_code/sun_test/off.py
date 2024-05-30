#!/usr/bin/env python3

# Warning: Only try this in simulation!
#          The direct attitude interface is a low level interface to be used
#          with caution. On real vehicles the thrust values are likely not
#          adjusted properly and you need to close the loop using altitude.

import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, VelocityNedYaw)
import socket

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(("192.168.232.137",65433))

async def run():
    """ Does Offboard control using attitude commands. """
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: \
              {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    # print("-- Go up 2 m/s")
    # await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, -2.0, 0.0))
    # await asyncio.sleep(4)

    # print("-- Go North 2 m/s, turn to face East")
    # await drone.offboard.set_velocity_ned(VelocityNedYaw(2.0, 0.0, 0.0, 90.0))
    # await asyncio.sleep(4)

    # print("-- Go South 2 m/s, turn to face West")
    # await drone.offboard.set_velocity_ned(
    #     VelocityNedYaw(-2.0, 0.0, 0.0, 270.0))
    # await asyncio.sleep(4)

    # print("-- Go West 2 m/s, turn to face East")
    # await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, -2.0, 0.0, 90.0))
    # await asyncio.sleep(4)

    # print("-- Go East 2 m/s")
    # await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 2.0, 0.0, 90.0))
    # await asyncio.sleep(4)

    # print("-- Turn to face South")
    # await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, 180.0))
    # await asyncio.sleep(2)

    # print("-- Go down 1 m/s, turn to face North")
    # await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 1.0, 0.0))
    # await asyncio.sleep(4)
    while True:
        try:
            data=sock.recv(300).decode()
            data=data.split(" ")
            print(data)
            yaw=float(data[0])
            throttle=float(data[1])
            roll=float(data[2])
            pitch=float(data[3]) 
            await drone.offboard.set_velocity_ned(VelocityNedYaw(pitch,roll,throttle,yaw))
            await asyncio.sleep(0.1)
        except Exception as e:
            print(e) 
    # print("-- Stopping offboard")
    # try:
    #     await drone.offboard.stop()
    # except OffboardError as error:
    #     print(f"Stopping offboard mode failed with error code: \
    #           {error._result.result}")




if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())