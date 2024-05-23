import time
import cv2
from model.pilot_model import *
from model.video_mode import *
import threading
import numpy as np
import pyrealsense2.pyrealsense2 as rs

class CameraController():
    def __init__(self,model:VideoModel,pilot_model:PilotModel) -> None:
        self.__model=model
        self.__pilot_model=pilot_model
        self.__picam2=self.__model.get_picam()
        self.__now_mode="gps"
        self.pipeline=rs.pipeline()
        self.config=rs.config()
        self.__init_realsense()
    
    def __init_realsense(self):
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = self.config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))
        #bgr
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    def run_fpv_cam(self):
        self.__picam2.start()  #picamera 시작한다.
        while True:
            if(self.__model.get_end_flag()==True):
                self.__model.set_end_flag(False)
                print('end this THread !!!!!!!!!!!!!!!')
                self.__picam2.stop()
                return
            frame=self.__picam2.capture_array()
            self.__model.set_raw_frame(frame) 
            self.__model.set_send_frame(frame)  #보내야할 찐도베이 frame이고
                
    def run_object_cam(self):
        raw_frame=None
        self.pipeline.start(self.config)
        while True:
            if(self.__model.get_end_flag()==True):
                print("end this Thread pipline")
                self.pipeline.stop()
                self.__model.set_end_flag(False)
                return
            frames=self.pipeline.wait_for_frames()
            color_frame=frames.get_color_frame()
            raw_frame = np.asanyarray(color_frame.get_data())
            self.__model.set_raw_frame(raw_frame)
            bbox_frame=self.__model.get_frame()
            self.__model.set_send_frame(bbox_frame)
            
    def run(self):
        time.sleep(3)
        while True:
            recv_mode=self.__pilot_model.get_data()[1] #현재 모드를 가져와서 변경됨을 확인한다.
            if self.__now_mode=="gps" and recv_mode=="manual":  
                self.__model.set_end_flag(True)
                time.sleep(0.3)
                self.__now_mode="manual"
                self.__model.now_mode="manual"
                thread_fpv=threading.Thread(target=self.run_fpv_cam)
                self.__model.set_end_flag(False)
                thread_fpv.start()
            elif self.__now_mode=="manual" and (recv_mode=="gps" or recv_mode=="tracker"):
                self.__model.set_end_flag(True)
                time.sleep(0.3)
                print("swap camera") 
                self.__now_mode="gps"
                self.__model.now_mode="gps"
                thread_gps=threading.Thread(target=self.run_object_cam)
                self.__model.set_end_flag(False)
                thread_gps.start()