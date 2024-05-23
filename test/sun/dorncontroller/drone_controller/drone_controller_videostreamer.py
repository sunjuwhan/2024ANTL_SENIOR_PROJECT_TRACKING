import cv2
import numpy as np
import socket
import numpy
from drone_controller.drone_controller_information import *
AP_IP="192.168.32.1"
PORT=8005
MY_IP="192.168.50.15"
BUFFER_SIZE=46081
class class_Drone_Controller_VideoStreamer:
    def __init__(self, info:class_Drone_Controller_Information):
        self.ip_address = AP_IP   #내 ip   ap로
        self.port = PORT  #고정
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip_address, self.port))
        self.info=info
    def assemble_image(self,slices):
        return np.vstack(slices)
    def receive_video(self):
        frames = [b'' for _ in range(20)]
        while True:
            
            size=0
            if self.info.now_mode=="manual":
                size=5
            else:
                size=20
            picture = b''
            #self.info.now_mode="manual"
            data, addr = self.socket.recvfrom(46081)  # 각 패킷은 46081바이트
            frames[data[0]] = data[1:46081]  # 수신된 프레임 데이터 저장
            if data[0] == size-1:  # 모든 패킷을 다 받았을 때
                for i in range(size):
                    picture += frames[i]  # 모든 프레임 데이터를 하나로 합침

                # 바이트 스트링을 numpy 배열로 변환하고 이미지로 디코딩
                try:
                    frame = cv2.imdecode(np.frombuffer(picture, dtype=np.uint8), cv2.IMREAD_COLOR)

# 이미지를 640x480 크기로 변환합니다.
                    #if self.info.now_mode=="manual":
                    frame= cv2.resize(frame, (640, 480))
# 변환된 이미지를 화면에 표시합니다.
                    cv2.imshow('Resized Image', frame)
                    #self.info.frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
                    self.info.display.update_video(frame)
                #self.info.frame = frame
                # 프레임 표시 시간 계산
                except Exception as e:
                    print(e)

                # 'q' 키를 누르면 종료
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
    def run_VideoStreamer(self):
        self.receive_video()