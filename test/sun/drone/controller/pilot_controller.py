import asyncio
from model.pilot_model import *
from model.gps_model import *
import time
from mavsdk.offboard import (OffboardError, PositionNedYaw)
class PilotController:
    def __init__(self,pilotmodel:PilotModel,gpsmodel:GpsModel,tracker_model=tracker_model) -> None:
        self.__pilot_model=pilotmodel  
        self.__drone=Drone()
        self.__gps_model= gpsmodel
        self.__tracker_model=tracker_model
        self.flag_arm=""

    async def init_dron(self):  #자자 이친구 잘 꺼내씁니다. return 해서 써 
        await self.__drone.make_drone()
        pass
    def get_dron_from_controller(self):
        return self.__drone.get_drone()
    
    def __recv_data(self,key,mode): #master 부터 recv해서 드론 컨트롤 하는 부분 
        self.__pilot_model.set_data(key,mode)
        
    async def get_gps(self) :
        
        async for position in self.__drone.get_drone().telemetry.position():
            self.__gps_model.set_gps(position.latitude_deg,position.longitude_deg,position.absolute_altitude_m,
                                     position.relative_altitude_m)
    async def get_text(self):
        async for st_text in self.__drone.get_drone().telemetry.status_text():
            print("Status Text : ",st_text)
    async def run(self):
        time.sleep(2)
        asyncio.ensure_future(self.get_gps())
        asyncio.ensure_future(self.get_text())
        st_latitude,st_longitude=self.__gps_model.get_gps()[0:2]
        self.__gps_model.set_start_gps(st_latitude,st_longitude)
        while True:
            (key,mode)=self.__pilot_model.get_data()
            (yaw,throttle,roll,pitch)=key.get_key()
            #print(mode,"  ",yaw,throttle,roll,pitch)
            if (mode=="arm"):
                try:
                    if self.flag_arm!="arm":
                        print("-- Arming")
                        await self.__drone.get_drone().action.arm()
                        await asyncio.sleep(3)
                        self.__pilot_model.set_drone_state("arm")
                        print("-- success Arming") 
                        await self.__drone.get_drone().action.takeoff()
                        await asyncio.sleep(3)
                        print("success Takeoff")
                        self.flag_arm="arm"
                except Exception as e:
                    print(e)
                    
            elif (mode=="takeoff") :
                try:
                    print("--  Takeoff")
                    await self.__drone.get_drone().action.set_takeoff_altitude(3.0)
                    await self.__drone.get_drone().action.takeoff()
                    await asyncio.sleep(3)
                    print(" --sucesse takeoff") 
                except Exception as e:
                    print(e)
                    
            elif (mode=="land"):
                try:
                    if self.flag_arm!="land":
                        print("-- land")
                        await self.__drone.get_drone().action.land()
                        await asyncio.sleep(5)
                        print("-- success landing")
                        self.__pilot_model.set_drone_state("land")  #착륙이 완료되었다는 신호를 보내줘
                        self.flag_arm=="land" 
                except Exception as e:
                    print(e)
                    
            elif( mode=="disarm" and self.__pilot_model.get_drone_state()!="init"): #맨처음 init일때는 할필요는 없고 나중에 이제 다른 모드일때 끄는거지
                try:
                    print("--disarm land")
                    await self.__drone.get_drone().action.kill()
                    await asyncio.sleep(5)
                    self.__pilot_model.set_drone_state("init")
                except Exception as e:
                    print(e)
            
            elif (mode=="manual"):
                self.flag_arm="manual"
                try:
                    
                    if(throttle>0.7):
                        throttle=0.7
                        
                    if(pitch>0.75):
                        pitch=0.75
                    elif pitch<-0.75:
                        pitch=-0.75
                   
                    if roll >0.75:
                        roll=0.75
                    elif roll<-0.75:
                        roll=-0.75
                    
                    await self.__drone.get_drone().manual_control.set_manual_control_input(pitch,roll,throttle,yaw)
                except Exception as e:
                    await self.__drone.get_drone().manual_control.set_manual_control_input(0.0,0.0,0.5,0.0)
                    await asyncio.sleep(0.1)
                    print(e)
            elif(mode=="tracker") :
                self.flag_arm="tracker"
                if(self.__tracker_model.get_flag()) :#object deteciton했을경우
                    pitch,yaw,throttle,roll=self.__tracker_model.get_manual_input()
                    print("Traking Value :    ",pitch,"  ",yaw,"  ",throttle,"  ",roll)
                    await self.__drone.get_drone().manual_control.set_manual_control_input(pitch,roll,throttle,yaw)
                    await asyncio.sleep(0.1)
                else:
                    print("Traking Value :  No Detection")
                    await self.__drone.get_drone().manual_control.set_manual_control_input(0.0,0.0,0.5,0.0)
                    await asyncio.sleep(0.1)
                    
            elif (mode=="gps") : #gps mode
                self.flag_arm="gps"
                now_latitude =self.__gps_model.get_gps()[0]
                now_longitude=self.__gps_model.get_gps()[1]
                now_height=self.__gps_model.get_gps()[3]
                count=0
                # try:
                #     await self.__drone.get_drone().offboard.set_position_ned(PositionNedYaw(0.0,0.0,0.0,0.0))  #setting 하는 곳 
                #     await self.__drone.get_drone().offboard.start() #순서 바꿔봤음
                # except OffboardError as error:
                #     print(f"Starting offboard mode failed \
                #     with error code: {error._result.result}")
                #     await self.__drone.get_drone().action.land()
                #y=0
                #x=0
                while True:
                    (a,chk_now_mode)=self.__pilot_model.get_data()
                    if(chk_now_mode!="gps"):
                        break 
                    try:
                        if count==0:
                            await self.__drone.get_drone().action.goto_location(now_latitude,now_longitude,self.__drone.flying_alt,0)
                            await asyncio.sleep(3)
                            print("drone hold mode")
                            await self.__drone.get_drone().action.hold()
                            await asyncio.sleep(1)
                            count+=1
                        else:
                            pass
                        
                    except Exception as e:
                        print(e)
                        
            elif (mode=="comback"):
                try:
                    await self.__drone.get_drone().action.goto_location(st_latitude,st_longitude,self.__drone.flying_alt-3,0)
                    await asyncio.sleep(10)
                except Exception as e:
                    print(e)
                