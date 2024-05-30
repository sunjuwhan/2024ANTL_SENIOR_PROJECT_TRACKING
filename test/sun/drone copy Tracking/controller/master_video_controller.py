from controller.pilot_controller import *
from controller.camera_controller import *
from model.pilot_model import *
from model.video_mode import *
from model.gps_model import *
class Master_video_controller():
    def __init__(self,pilot_model:PilotModel,video_model:VideoModel,gps_model:GpsModel,tracker_model:tracker_model) : 
        self.__pilot_model=pilot_model
        self.__camera_model=video_model
        self.__camera_controller=CameraController(self.__camera_model,self.__pilot_model)
    def run_camera(self):
        self.__camera_controller.run()
        