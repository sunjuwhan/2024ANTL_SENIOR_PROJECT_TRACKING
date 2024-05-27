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
        print("1")
        self.__pilot_model=model.PilotModel()
        print("2")
        self.__camera_model=model.VideoModel() 

        print("3")
        self.__gps_model=model.GpsModel()
        
        print("4")
        self.__tracker_model=model.tracker_model()

        print("5")
        self.__controller=controller.Master_video_controller(self.__pilot_model,self.__camera_model,self.__gps_model,self.__tracker_model)

        print("6")
        self.__view= view.SocketView(self.__pilot_model,self.__camera_model,self.__gps_model)
        
        print("7")
        self.__object=controller.ObjectController(self.__camera_model,self.__tracker_model)  
        
        print("8")
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
        print("a")
        self.__pilot_model=model.PilotModel()
        print('b')
        self.__gps_model=model.GpsModel()
        print('c')
        self.__controller=controller.Master_drone_Controller(self.__pilot_model,self.__gps_model)
        print('d')
        self.__view= view.Socket_view_drone(self.__pilot_model,self.__gps_model)
        print('d')
        
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
    main_drone.run_drone_main() 
    
if __name__ == "__main__":
    with Pool(processes=2) as pool:  # 2개의 프로세스로 풀을 만듭니다.
        print("Start Multi Processing Drone")
        
        result_A = pool.apply_async(run_camera)
        result_B = pool.apply_async(run_drone)
        # 결과를 기다립니다.
        result_A.wait()
        result_B.wait()
    print("now")

