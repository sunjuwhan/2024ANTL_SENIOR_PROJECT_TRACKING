from multiprocessing import Pool,Manager
from main_camera import *
from main import *
import os


import controller
import model
import view 
import asyncio
from threading import *
import time


class MainCamera():
    def __init__(self) -> None:
        self.__pilot_model=model.PilotModel()
        self.__camera_model=model.VideoModel() 
        self.__gps_model=model.GpsModel()
        self.__tracker_model=model.tracker_model()
        self.__controller=controller.Master_video_controller(self.__pilot_model,self.__camera_model,self.__gps_model,self.__tracker_model)
        self.__view= view.SocketView(self.__pilot_model,self.__camera_model,self.__gps_model)
        self.__object=controller.ObjectController(self.__camera_model,self.__tracker_model)  
    def run(self,shard_data):
        print("run object Detecter ")
        dectetor_thread=Thread(target=self.__object.run_object_detector) 
        dectetor_thread.start()
        print("run camera thread")
        camera_thread=Thread(target=self.__controller.run_camera)
        camera_thread.start()
        print("camera Thread Running ")
        time.sleep(3)
        self.__view.run_camera()
        print("end camera & socket setting ")
        shared_data['key'] =True
        
        
    async def run_pilot(self) :
        await self.__controller.run_pilot()
    def run_camera_main(self,shared_data):
        print("camer Processe start")
        self.run(shared_data)
        
        
class MainDrone():
    def __init__(self) -> None:
        self.__pilot_model=model.PilotModel()
        self.__gps_model=model.GpsModel()
        self.__controller=controller.Master_drone_Controller(self.__pilot_model,self.__gps_model)
        self.__view= view.Socket_view_drone(self.__pilot_model,self.__gps_model)
        
    def run(self):
        self.__view.run_drone()
        print("end camera & socket setting ")
    async def run_pilot(self) :
        await self.__controller.run_pilot()
    async def run_drone_main(self):
        print("start main Function")
        self.run()
        asyncio.run(self.run_pilot())       

def run_camera():
    main_camera=MainCamera()
    main_camera.run_camera_main(shared_data)

def run_drone(shared_data):
    while True:
        if 'key' in shared_data:
            break
        
        
    main_drone=MainDrone()
    main_drone.run()
    asyncio.run(main_drone.run_pilot()) 
    
if __name__ == "__main__":
    with Manager() as manager:
        shared_data=manager.dict()
        with Pool(2) as p:
            
    #p=Pool(2)
            result_A=p.apply_async(run_camera,(shared_data,))
            result_B=p.apply_async(run_drone,(shared_data,))
            p.close()
            p.join()
    
    
    

