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
#if __name__=="__main__":
#    main_function=Main()
#    print("start")
#    main_function.run()
    #asyncio.run(main_function.run_pilot())
        
        