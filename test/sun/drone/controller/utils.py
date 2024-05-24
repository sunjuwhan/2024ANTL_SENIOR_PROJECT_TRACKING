import cv2
import numpy as np
from PIL import Image
from controller.constant import *

    
class Image_Manager:
    def __init__(self):
        self.frame = None # 3차원 행렬
        self.width = 0
        self.height = 0
        self.init_flag = False
    # 이번 루프에서 프레임 특징
    def recog_image(self, frame):
        self.frame = frame
        #self.frame = cv2.flip(self.frame, 0)
        #self.frame= cv2.flip(self.frame, 1)

        cv2_im_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) # 주석 처리

        cv2_im_rgb=self.frame
        pil_im = Image.fromarray(cv2_im_rgb)
        # 최초에 한번만 연산
        if not self.init_flag:
            self.height, self.width = frame.shape
            self.init_flag = True
            
        return self.width, self.height, pil_im
    
    def show_test_window(self):
        cv2.imshow('test_window', self.frame)
        return

    def get_frame(self):
        return self.frame
    
    def set_frame(self, frame):
        self.frame = frame

    #def depth_draw(self, x, y, depth):
        #self.frame = self.bbox_manager.draw_depth_in_image(self.frame, x, y, depth)
        #return 

    # bbox 만들기
    def append_text_img(self, objs, labels):
        height, width, _= self.frame.shape

        #fps=round(100/dur,1)
        #fps 조정 = 1000/전체 작동시간

        self.frame= cv2.rectangle(self.frame, (0,0), (width, 24), (0,0,0), -1)
        #cv2 외부 틀만들기

        #text1 = 'FPS: {}'.format(dur)
        
        #self.frame = cv2.putText(self.frame, text1, (10, 20),FONT, 0.7, (0, 0, 255), 2)
        
        #아래는 대충 사각형으로 오브젝트를 감싸는 내용
        for obj in objs:
            x0, y0, x1, y1 = list(obj.bbox)
            x0, y0, x1, y1 = int(x0*width), int(y0*height), int(x1*width), int(y1*height)
            percent = int(100 * obj.score)
            if (percent>=60):
                box_color, text_color, thickness=(0,255,0), (0,255,0),2
            elif (percent<60 and percent>40):
                box_color, text_color, thickness=(0,0,255), (0,0,255),2
            else:
                box_color, text_color, thickness=(255,0,0), (255,0,0),1
            text3 = '{}% {}'.format(percent, labels.get(obj.id, obj.id)) #얼마나 일치하는지 표시
            self.frame = cv2.rectangle(self.frame, (x0, y0), (x1, y1), box_color, thickness)
            self.frame = cv2.putText(self.frame, text3, (x0, y1-5),FONT, 0.5, text_color, thickness)
        return 
    
        
        