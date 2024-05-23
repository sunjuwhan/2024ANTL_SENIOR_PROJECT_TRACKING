
from controller.common import *
from controller.constant import *
from controller.utils import *
import cv2
import numpy as np
from threading import Thread
import time

from model import VideoModel


class ObjectController:
    def __init__(self, video_model,tracker_model:tracker_model):
        self.__key = []
        self.__video_model:VideoModel = video_model# 카메라 정보 
        #self.__mode:ModeModel = mode
        self.status = 0 # 0 : 정지, 1 : 동작, 2 : 일시정지
        self.pause_flag = False
        self.__tracker_model=tracker_model
        self.tool = Tools(self.__tracker_model) # 로드 모델, 로드 라벨, 텐서 세팅
        self.image_manager = Image_Manager()
        self.__object_follower = ObjectFollower(key=self.__key) # 검색 시작

    def __human_detection(self):
        # 라벨 세팅
        #distance = []
        fps = 1
        #반복되는 핵심 와일문
        time.sleep(7)        
        while True:
            if self.__video_model.now_mode=="manual":  #manual 모드이면 일시정지 해주고
                continue

            start_time = time.time()            
            frame = self.__video_model.get_raw_frame()
            _, _, pil_im = self.image_manager.recog_image(frame)

            # 연산 부분
            self.tool.set_input(pil_im)
            objs = self.tool.get_output() # obj 탐색

            # output을 바탕으로 사용가능한 bbox인지 체크 및 그리기
            
            # 발견한 오브젝트의 거리를 분석
            try:
                self.__object_follower.check_object(objs=objs, frame=frame)
            except Exception as e:
                print("ERROR :: follower did not work")
                print(e)

            fps = round(1.0/(time.time() - start_time), 1)
            self.image_manager.append_text_img(objs=objs,
                                               labels=self.tool.get_labels(),
                                               dur=fps)          
            # bbox된 이미지 데이터를 다시 카메라 프레임으로 설정
            bboxed_frame = self.image_manager.get_frame()
            self.__video_model.set_frame2bboxed_frame(bboxed_frame)
    
    # 실행기
    def run_object_detector(self):
        self.status = 1 # 텐서 연산을 한다 : 1, 안한다 : 2
        human_detector_thread = Thread(target=self.__human_detection)
        human_detector_thread.start()
    
    def get_key(self):
        
        return self.__key

