import controller
import model
import view 
import asyncio
from threading import *
import time

import view

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
        
#if __name__=="__main__":
#    main_function=Main()
#    print("start")
#    main_function.run()
#    asyncio.run(main_function.run_pilot())
        
        
    