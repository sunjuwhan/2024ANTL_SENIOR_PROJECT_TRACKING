from multiprocessing import Pool
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
    def run(self):
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
        
    async def run_pilot(self) :
        await self.__controller.run_pilot()
    def run_camera_main(self):
        print("camer Processe start")
        self.run()
        
        
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
    main_camera.run_camera_main()

def run_drone():
    main_drone=MainDrone()
    main_drone.run()
    asyncio.run(main_drone.run_pilot()) 
    
if __name__ == "__main__":
    p=Pool(2)
    result_A=p.apply_async(run_camera,)
    result_B=p.apply_async(run_drone,)
    p.close()
    p.join()
    
    
    

