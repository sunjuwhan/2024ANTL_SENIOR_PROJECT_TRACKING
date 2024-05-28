
import asyncio
from mavsdk import System

class Drone:
    def __init__(self) -> None:
        self.antl_drone = None
        self.flying_alt=None
    async def make_drone(self):
        
        self.antl_drone=System()
        print("wating connect drone")
        await self.antl_drone.connect(system_address="serial:///dev/ttyAMA0")
        
        
        #await self.antl_drone.connect(system_address="udp://:14540")
        
        print("Start connect") 
        #await self.antl_drone.connect(system_address="udp://:14540")
        print("Wating for drone to connect...")  #drone connect 
        
        async for state in self.antl_drone.core.connection_state():
            if state.is_connected:
                print(f"-- Connected to drone!")
                break
            
        #async for health in self.antl_drone.telemetry.health():
        #    if health.is_global_position_ok and health.is_home_position_ok:
        #        print("-- Global position state is good enough for flying.")
        #        break
        #try:
        #    await self.antl_drone.manual_control.set_manual_control_input
        #    (float(0), float(0), float(0.5), float(0))
        #    print("good")
            
        #except Exception as e:
        #    print(e)
            
            
        #print("Fetching amsl altitude at home location....")
        #async for terrain_info in self.antl_drone.telemetry.home():
            #absolute_altitude = terrain_info.absolute_altitude_m
            #break
        
        #self.flying_alt=absolute_altitude+6
        #print('======================self.flying alt')
        #print(self.flying_alt)
        
        self.flying_alt=6  
        #print("-- Arming")
        #await self.antl_drone.action.arm()
        #await asyncio.sleep(1)
        
        #print("--take off")
        #await self.antl_drone.action.takeoff()
        #await asyncio.sleep(5)

    def get_drone(self):
        return self.antl_drone
class Key:#
    def __init__(self):
        self.__yaw = 0
        self.__throttle = 0
        self.__pitch = 0
        self.__roll = 0
    ##set
    def set_key(self,yaw,throttle,pitch,roll):
        self.__yaw=yaw
        self.__throttle=throttle
        self.__pitch=pitch
        self.__roll=roll
    ##get
    def get_key(self):
        return (self.__yaw,self.__throttle,self.__roll,self.__pitch)


class PilotModel:
    def __init__(self):
        self.__key = Key()
        self.__mode = 0
        self.__drone_state="init"
    def set_mode(self, mode):  
        self.__mode = mode
        return

    def set_data(self, key,mode):
        try:
            self.__key.set_key(
                yaw=float(key[0]), throttle=float(key[1]), 
                pitch=float(key[2]), roll=float(key[3])
                )
            self.__mode=mode
        except:
            print("ERROR :: Bad key request")
            self.__key.set_key(
                yaw=float(0), throttle=float(0.5), 
                pitch=float(0), roll=float(0)
                )
        return 

    def set_drone_state(self,state):
        self.__drone_state=state
        
    def get_drone_state(self):
        return self.__drone_state
        
    def get_key(self):
        return self.__key.get_key()
    
    def get_mode(self):
        return self.__mode

    def get_data(self):
        return (self.__key,self.__mode)

class tracker_model:
    def __init__(self) -> None:
        self.__yaw=0.0
        self.__pitch=0.0
        self.__throttle=0.5
        self.__roll=0.0
        self.__xmin=None
        self.__xmax=None
        self.__ymin=None
        self.__ymax=None
        self.__chk_object=False
        self.__roll_gain=0.3   #좌우로 움직일 gain값
        self.__pitch_gain=0.25  #상하로 움직일 gain값
        
    def set_bbox(self,xmin,ymin,xmax,ymax):
        self.__xmin=xmin *640
        self.__xmax=xmax *640
        self.__ymin=ymin *320
        self.__ymax=ymax *320
        self.cal_distance()  #update가 되면 cal_distacne를 수행한다 
        
    def set_flag(self,flag) :
        self.__chk_object=flag
        
        
    def set_manual_input(self,pitch,roll):
        self.__pitch=pitch
        self.__roll=roll 
    
    def get_flag(self) :
        return self.__chk_object
    def get_manual_input(self):
        return(self.__pitch,self.__yaw,self.__throttle,self.__roll)
    
    def cal_distance(self):
        #문제는 드론의 시야 각 고정을 어디로 했냐에 따라서 이거는 바뀜 roll을 어떻게 돌려야할지에 대한 판단이 서야함   (해결 완료)
        """
        거리에 따른 모터 세기값을 구하기위해
        x축은 거리 /320 * gain(모터의 최대 갑을 대입)  가로는 0.3 세로는 0.25로 측정하고
        y축은 거리 / 240 * gain()
        방향 벡터 구해서 계산 하는 방식으로 진행
        """
        try:
            mid_x=(self.__xmin+self.__xmax)/2
            mid_y=(self.__ymin+self.__ymax)/2
            
            if 300<=mid_x and mid_x<=340 and 230<=mid_y and mid_y<=250:
                self.__yaw=0.0
                self.__pitch=0.0
                self.__throttle=0.5
                self.__roll=0.0
                
            else:  # 내 시야각 중앙점에 안들어오고 멀리 떨어져있을경우
                diff_roll= (abs(mid_x-320)/320)*self.__roll_gain   #gain값이 0.3
                diff_pitch = (abs(mid_y-240)/240)*self.__pitch_gain  #gain값이 0.25
                if mid_x<=320:  #왼쪽지점으로 가있을경우  roll 값이 왼쪽이니까 -로 넣어줘야함
                    diff_roll=-diff_roll
                    if mid_y>240:  #아래쪽이까 pitch - 값
                        diff_pitch=-diff_pitch
                elif mid_x>320:  #오른쪽 지점으로 가있을경우  roll값은 +로 
                    if mid_y>240:  #아래쪽이동 하니까 pitch - 값
                        diff_pitch=-diff_pitch 
            self.set_manual_input(diff_pitch,diff_roll)
            
        except Exception as e:
            self.set_manual_input(0.0,0.0)
            print(e)
        
    