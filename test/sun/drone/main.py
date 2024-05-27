import controller
import model
import view 
import asyncio
from threading import *
import time
class Main():
    def __init__(self) -> None:

        self.__pilot_model=model.PilotModel()
        self.__camera_model=model.VideoModel() 
        self.__gps_model=model.GpsModel()
        self.__tracker_model=model.tracker_model()
        
        self.__controller=controller.MasterController(self.__pilot_model,self.__camera_model,self.__gps_model,self.__tracker_model)
        self.__view= view.SocketView(self.__pilot_model,self.__camera_model,self.__gps_model)
        
        self.__object=controller.ObjectController(self.__camera_model,self.__tracker_model)  
    def run(self):
        #print("run object Detecter ")
        #dectetor_thread=Thread(target=self.__object.run_object_detector) 
        #dectetor_thread.start()
        #print("run camera thread")
        #camera_thread=Thread(target=self.__controller.run_camera)
        #camera_thread.start()
        #print("camera Thread Running ")
        #time.sleep(3)
        self.__view.run_drone()
        print("end camera & socket setting ")
        
    async def run_pilot(self) :
        await self.__controller.run_pilot()
        
if __name__=="__main__":
    main_function=Main()
    print("start")
    main_function.run()
    asyncio.run(main_function.run_pilot())
        
        
    