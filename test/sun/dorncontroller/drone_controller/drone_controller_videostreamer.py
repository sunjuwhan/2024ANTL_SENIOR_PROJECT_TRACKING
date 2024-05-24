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
        self.buffer={}
    def assemble_image(self,slices):
        return np.vstack(slices)
    def receive_video(self):
        frames = [b'' for _ in range(20)]
        while True:
            
            packet, _ = self.socket.recvfrom(65536)
            packet_id = packet[0]
            data = packet[1:]
            
            self.buffer[packet_id] = data
            
            # 패킷 ID가 0이면 프레임 재구성 시도
            if packet_id == 0:
                frame_data = b''.join([self.buffer[i] for i in sorted(self.buffer.keys()) if i in buffer])
                frame = np.frombuffer(frame_data, dtype=np.uint8)
                #frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                #if frame is not None:
                #    cv2.imshow('Received Video', frame)
                
                #if cv2.waitKey(1) & 0xFF == ord('q'):
                #    break
                self.buffer.clear()
# 이미지를 640x480 크기로 변환합니다.
                    #if self.info.now_mode=="manual":
                frame= cv2.resize(frame, (640, 480))
# 변환된 이미지를 화면에 표시합니다.
                    #cv2.imshow('Resized Image', frame)
                    #self.info.frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
                self.info.display.update_video(frame)
                #self.info.frame = frame
                # 프레임 표시 시간 계산
                # 'q' 키를 누르면 종료
                #if cv2.waitKey(1) & 0xFF == ord('q'):
                #    cv2.destroyAllWindows()
                #    break
    def run_VideoStreamer(self):
        self.receive_video()