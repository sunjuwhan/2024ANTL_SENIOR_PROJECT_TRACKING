#!/usr/bin/env python3

"""
Caveat when attempting to run the examples in non-gps environments:

`drone.offboard.stop()` will return a `COMMAND_DENIED` result because it
requires a mode switch to HOLD, something that is currently not supported in a
non-gps environment.
"""

import asyncio
import socket
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)
from threading import Thread
from math import radians, sin, cos, sqrt, atan2, degrees
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(("192.168.232.138",8000))
sock.listen(1)
client_sock,addr=sock.accept()


class joystick:
    def __init__(self) -> None:
        self.__yaw=None
        self.__pitch=None
        self.__roll=None
        self.__throttle=None
        self.__mode=None
    def set_joystick(self,yaw,throttle,roll,pitch,mode):
        self.__yaw=float(yaw)
        self.__throttle=float(throttle)
        self.__roll=float(roll)
        self.__pitch=float(pitch)
        self.__mode=mode
    def get_joystick(self):
        return (self.__yaw,self.__throttle,self.__roll,self.__pitch,self.__mode)
class GpsModel:
    def __init__(self) -> None:
        self.__latitude_deg=None #위도
        self.__longitude_deg=None #경도
        self.__absolute_altitude=None  
        self.__relative_altitude=None  #실제 높이 
    def set_gps(self,latitude,longitude,absolute,relative):
        self.__latitude_deg=latitude
        self.__longitude_deg=longitude
        self.__absolute_altitude=absolute
        self.__relative_altitude=relative
        

    def get_gps(self):
        return(self.__latitude_deg,self.__longitude_deg,self.__absolute_altitude,self.__relative_altitude)
class recv_Data:
    def __init__(self) -> None:
        self.recv_data="init" 
        
        
recv_class=recv_Data() 
        
def get_direction(start_lat, start_lon, end_lat, end_lon):
    # 위도와 경도의 차이 계산
    dlat = end_lat - start_lat
    dlon = end_lon - start_lon

    # x축과 y축 방향 계산
    x_distance = dlon * 111319.9 * cos(radians(start_lat))  # 1도의 경도 차이는 적도에서 약 111319.9 미터
    y_distance = dlat * 111319.9  # 1도의 위도 차이는 항상 약 111319.9 미터

    return x_distance, y_distance 
def get_distance(lat1, lon1, lat2, lon2):
    # 지구의 반지름 (미터 단위)
    R = 6371000.0

    # 위도 및 경도를 라디안으로 변환
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(radians, [lat1, lon1, lat2, lon2])

    # 두 지점 간의 차이를 계산
    delta_lon = lon2_rad - lon1_rad
    delta_lat = lat2_rad - lat1_rad

    # x축과 y축으로의 거리 계산
    x = R * delta_lon * cos((lat1_rad + lat2_rad) / 2)
    y = R * delta_lat

    return x, y
from math import radians, sin, cos, sqrt, atan2






# # 예시 좌표
# lat1 = 37.7749
# lon1 = -122.4194
# lat2 = 34.0522
# lon2 = -118.2437

# x_distance, y_distance = get_distance(lat1, lon1, lat2, lon2)
# bearing = get_bearing(lat1, lon1, lat2, lon2)
# print("두 지점 간의 각도는 {:.2f} 도입니다.".format(bearing))
# print("x축으로 {:.2f} 미터, y축으로 {:.2f} 미터 이동해야 합니다.".format(x_distance, y_distance))
joystick_model=joystick()
async def run_text(drone):
    async for st_text in drone.telemetry.status_text():
        print("CUSTOM StatusText:  ",st_text)
        
async def run():
    
    """ Does Offboard control using position NED coordinates. """

    drone = System()
    gps_mode=GpsModel()
    await drone.connect(system_address="udp://:14540")
    
    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break
        
        
    asyncio.ensure_future(get_gps(drone,gps_mode))
    asyncio.ensure_future(run_text(drone))
    
    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break
        
        
        
    print("Fetching amsl altitude at home location....")
    async for terrain_info in drone.telemetry.home():
        absolute_altitude = terrain_info.absolute_altitude_m
        break
    
    flying_alt = absolute_altitude + 5.0
    
    print("-- Arming")
    await drone.action.arm()
    await asyncio.sleep(5)
    print("--takeoff")

    await drone.action.takeoff()
    await asyncio.sleep(5)
    try:
        await drone.manual_control.set_manual_control_input(
        float(0), float(0), float(0.5), float(0)
    )
        print("good")
    except Exception as e:
        print(e)    
    #print("-- Setting initial setpoint")  #아 현재 위치를 setting 하는 작업이구나 그러면 현재 위치를 0,0,0,0 이라고 setpoint를 찍는거네 
    #await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    #print("-- Starting offboard")
    #try:
    #    await drone.offboard.start()
    #except OffboardError as error:
    #    print(f"Starting offboard mode failed \
    #            with error code: {error._result.result}")
    #    print("-- Disarming")
    #    await drone.action.disarm()
    #    return


    #asyncio.ensure_future(get_gps(drone,gps_mode))
    
    #await drone.offboard.set_position_ned(
    #        PositionNedYaw(0.0, 0.0, -5.0, 0.0))    
    #await asyncio.sleep(10)
    #    + 북 - 남    /     +동 - 서      /    +up - donw    /  각도는 시계방향으로 
    #print("-- Go 5m North, 0m East, -5m Down \
    #        within local coordinate system, turn to face East")
    #await drone.offboard.set_position_ned (PositionNedYaw(5.0, 0.0, -5.0, 0.0))  
    #await asyncio.sleep(10)
    
    # #여기까지 움직였다고 치고
    flag_mode=None
    while True:
        yaw,throttle,roll,pitch,mode=joystick_model.get_joystick() 
        if mode=="manual":
            try:
                recv_class.recv_data="manual"
                if(throttle>0.7):
                    throttle=0.7
                    
                if(pitch>0.7):
                    pitch=0.7
                elif pitch<-0.7:
                    pitch=-0.7
                
                if roll >0.7:
                    roll=0.7
                elif roll<-0.7:
                    roll=-0.7
                    
                await drone.manual_control.set_manual_control_input(pitch,roll,throttle,yaw)
            except Exception as e:
                await drone.manual_control.set_manual_control_input(0.0,0.0,0.5,0.0)
                print(e)
        elif mode=="arm":
            print("-- Arming")
            await drone.action.arm()
            await asyncio.sleep(5)
            recv_class.recv_data="arm"
        elif mode=="disarm" and recv_class.recv_data!="init":
            try:
                print("--disarm lan")
                await drone.action.kill()
                await asyncio.sleep(3)
                recv_class.recv_data="disarm" 
            except Exception as e:
                print(e)
        elif mode=="land":
            print('land')
            await drone.action.land()
            recv_class.recv_data="land"
            await asyncio.sleep(5)
        # elif mode=="gps":
        #     now_latitude=gps_mode.get_gps()[0]
        #     now_longitude=gps_mode.get_gps()[1]  #현재 위치 받아와서
        #     now_height=gps_mode.get_gps()[3]
        #     try:
        #         await drone.offboard.set_position_ned(PositionNedYaw(0.0,0.0,0.0,0.0))  #setting 하는 곳 
        #         await drone.offboard.start() #순서 바꿔봤음
        #     except OffboardError as error:
        #         print(f"Starting offboard mode failed \
        #         with error code: {error._result.result}")
        #         print("-- Disarming")
        #         await drone.action.disarm()
        #         return
        #     y=0
        #     x=0
        #     while True:  #모드가 gps인 동안 계속해서 작동해야한다.
        #         gps_mod_now=joystick_model.get_joystick()[4]
        #         if(gps_mod_now!="gps"):
        #             try:
        #                 await drone.offboard.stop()
        #                 print("success stop offboard")
        #             except Exception as e:
        #                 print(e)
        #             break
        #         try:
        #             await drone.offboard.set_position_ned(PositionNedYaw(get_direction(gps_mode.get_gps()[0],gps_mode.get_gps()[1],now_latitude,now_longitude)[1], get_direction(gps_mode.get_gps()[0],gps_mode.get_gps()[1],now_latitude,now_longitude)[0], -5.0,0.0))  #높이는 -5로 고정하고 
        #             #await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))
        #             await asyncio.sleep(4) 
        #             x,y=get_direction(gps_mode.get_gps()[0],gps_mode.get_gps()[1],now_latitude,now_longitude)
        #             print(f"x 축으로 {x}  만큼 y축으로 {y} 만큼 움직여야합니다.")
        #         except Exception as e:
        #             print(e)
        #     """
        #     gps 모드로 들어오면 현재 위치 받아서  저장한다음에 이제 계속 이위치로 가야해 언제까지? 모드가 바뀔때까지
        #     """
        elif mode=="gps":
            count=0
            now_latitude=gps_mode.get_gps()[0]
            now_longitude=gps_mode.get_gps()[1]  #현재 위치 받아와서
            now_height=gps_mode.get_gps()[3]
            recv_class.recv_data="gps"
            while True:
                gps_mod_now=joystick_model.get_joystick()[4]
                if(gps_mod_now!="gps"):
                    break
                try:
                    if count==0:
                        print(now_latitude,now_latitude)
                        await drone.action.goto_location(now_latitude,now_longitude,flying_alt,0)
                        await asyncio.sleep(4)
                        await drone.action.hold()
                        await asyncio.sleep(1)
                        count+=1
                    else:
                        pass
                except Exception as e:
                    pass
async def get_gps(drone,drone_model:GpsModel):
    async for position in drone.telemetry.position():
        drone_model.set_gps(position.latitude_deg,position.longitude_deg,position.absolute_altitude_m,
                                    position.relative_altitude_m)  #relative
def run_socket():
    while True:
        data=client_sock.recv(1024).decode().split(' ')
        joystick_model.set_joystick(data[0],data[1],data[2],data[3],data[4])
        send_Data="arm"
        client_sock.send(send_Data.encode())
if __name__ == "__main__":
    # Run the asyncio loop
    socket_trhead=Thread(target=run_socket)
    socket_trhead.start()
    asyncio.run(run())