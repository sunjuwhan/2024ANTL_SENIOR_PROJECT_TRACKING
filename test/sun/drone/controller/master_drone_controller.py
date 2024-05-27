from controller.pilot_controller import *
from model.pilot_model import *
from model.gps_model import *
class MasterController():
    def __init__(self,pilot_model:PilotModel,gps_model:GpsModel) : 
        self.__pilot_controller=None
        self.__pilot_model=pilot_model
        self.__gps_model=gps_model
        self.__drone=None
        self.__gps_controller=None
        
    async def run_pilot(self):    #asyncio .run()으로 실행하고 나머지는 thread로 실행해야할거같은데
        try:
            #print("init drone 주석 처리부분 시작")
            self.__pilot_controller=PilotController(self.__pilot_model,self.__gps_model,None)
            print("start init drone")
            await self.__pilot_controller.init_dron()
            self.__drone=self.__pilot_controller.get_dron_from_controller()  
            await self.__pilot_controller.run()  #controller 시작하고 
        except Exception as E:
            print(E)
            print("Asynci did Bad action !! __run_pilot")
        