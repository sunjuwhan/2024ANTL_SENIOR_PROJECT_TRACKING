from picamera2 import Picamera2

import cv2
class VideoModel():
    def __init__(self) -> None:
        #self.__cap=cv2.VideoCapture(0)
        #self.__cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        #self.__cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.__picam2=Picamera2()
        self.__picam2.preview_configuration.main.size = (320, 240)
        self.__picam2.preview_configuration.main.format = "RGB888"
        #self.__picam2.preview_configuration.main.format = "Y8"
        self.__picam2.preview_configuration.align()
        self.__picam2.configure("preview")
        #self.__picam2.start()
        self.__frame=None  #원본 진짜 그자체
        self.__raw_frame=None
        self.__image_slice=None
        self.__end_flag=False
        self.__send_frame=None
        self.now_mode="manual"
    def set_frame2bboxed_frame(self, frame):
        self.__frame = frame

    def set_frame2wait_image(self):
        self.__frame = self.__wait_img
        self.__raw_frame = self.__wait_img
        return

    def set_raw_frame(self, frame):  #진짜 원본
        self.__raw_frame = frame
        return 
    def get_send_frame(self) :
        return self.__send_frame
    def set_send_frame(self,frame):
        self.__send_frame=frame
        
        
        
    def set_frame(self,frame):   #BBOX 쳐진 사진
        self.__frame=frame
        
    def get_frame(self):
        return self.__frame
    
    def get_raw_frame(self):
        return self.__raw_frame
    
    def get_picam(self) :
        return self.__picam2
    
    
    def set_end_flag(self,end_flag):  #카메라 전환을 위한 flag
        self.__end_flag=end_flag
        
        
    def get_end_flag(self):
        return self.__end_flag
    
    
    
 
    def split_image(self, num_slices):
        slice_height = self.__frame.shape[0] // num_slices
        slices = []
        for i in range(num_slices):
            start = i * slice_height
            end = start + slice_height
            slices.append(self.__frame[start:end, :])
        return slices