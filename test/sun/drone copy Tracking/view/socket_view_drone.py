import numpy as np
from view.constant import *
from socket import *
from threading import *
from model.pilot_model import *
from view.constant import *
from model.gps_model import *
import socket
import time
import cv2
import struct
from picamera2 import Picamera2
class Socket_view_drone():
    def __init__(self,model:PilotModel,gps:GpsModel) -> None:
        self.video_socket=None
        self.pilot_socket=None
        self.__pilot_mode=model
        self.__video_model=None
        self.__client_socket=None 
        self.__gps_model=gps
        self.video_receve_socket=None
        
    def make_socket(self):
        self.video_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.video_receve_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  #영상 송수신을 위한 현재 드론 상태를 받을곳
        self.pilot_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.pilot_socket.bind((IP_DRONE,PORT_DRONE))   #여기는 내가 받아야하니까 내 주소 drone주소
            self.video_receve_socket.bind((IP_DRONE,PORT_DRONE))   #여기도 내가 영상 송수신을 위해 어떠한 type인지 받기 위한곳
            self.pilot_socket.listen(1)
            self.__client_socket,clien_address=self.pilot_socket.accept()
            print("make_socket end")
        except Exception as e:
            print("make_socket Error here")
            print(e)
            
            
            
    def make_socket_video(self):
        self.video_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.video_receve_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  #영상 송수신을 위한 현재 드론 상태를 받을곳
        try:
            self.video_receve_socket.bind((IP_DRONE,PORT_VIDEO))   #여기도 내가 영상 송수신을 위해 어떠한 type인지 받기 위한곳
        except Exception as e:
            print("make_socket Error video")
            print(e)
            
            
    def make_socket_drone(self):
        self.pilot_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.pilot_socket.bind((IP_DRONE,PORT_DRONE))   #여기는 내가 받아야하니까 내 주소 drone주소
            self.pilot_socket.listen(1)
            self.__client_socket,clien_address=self.pilot_socket.accept()
            print("make_socket end")
        except Exception as e:
            print("make_socket Error drone")
            print(e)
            
            
        
    def __data_send(self): #이미지 전송할 함수
        time.sleep(5)
        frame_id=0
        while True : 
            try:
                frame=self.__video_model.get_send_frame()  #46081
                now_mode=self.__pilot_mode.get_data()[1]  
                size_of_send=0

                if now_mode=="gps" or now_mode=="tracking":
                    size_of_send=15
                else:
                    size_of_send=4
                _, encoded_frame=cv2.imencode('.jpg',frame,[int(cv2.IMWRITE_JPEG_QUALITY),50])
                
                s=encoded_frame.tobytes()
                packet_size = 65507 - 3  # UDP 패킷 최대 크기 (식별자 바이트를 위해 1 바이트 제외)
                num_packets = len(s) // packet_size + (1 if len(s) % packet_size != 0 else 0)
                

                for i in range(num_packets):
                    packet_data = s[i*packet_size:(i+1)*packet_size]
                    packet = struct.pack("BH", i,frame_id) + packet_data
                    self.video_socket.sendto(bytes([i]) +s[i*65506:(i+1) *65506], (IP_CONTROLLER, PORT_CONTROLLER)) #46080
                frame_id=(frame_id+1) %65536
                #for i in range(num_packets):
                #    self.video_socket.sendto(bytes([i]) +s[i*65506:(i+1) *65506], (IP_CONTROLLER, PORT_CONTROLLER)) #46080
            except Exception as e:
                pass
    def __data_recv_cam(self):
        while True:
            try:
                recv_data=self.video_receve_socket.recv(1024)  #데이터 전달받고
                decoded_data=recv_data.decode()
                data=decoded_data.split(' ')
                key_data=data[0:4] 
                mode_data=data[4]
                #data 를 interface인 pilot_mode에다가 저장해주고
                self.__pilot_mode.set_data(key_data,mode_data)   #data만 저장해주고 
            except Exception as e:
                print(e)

    def __data_recv(self):  #여기서 drone의 상태랑 등등을 어차피 다 담아서 보내니까
        while True:
            try:
                recv_data=self.__client_socket.recv(1024)
                decoded_data=recv_data.decode()
                data=decoded_data.split(' ')
                key_data=data[0:4] 
                mode_data=data[4]
                #data 를 interface인 pilot_mode에다가 저장해주고
                self.__pilot_mode.set_data(key_data,mode_data) 
                try:
                    latitude=str(self.__gps_model.get_gps()[0])
                    longitude=str(self.__gps_model.get_gps()[1])
                    mode_gps=self.__pilot_mode.get_drone_state()+' '+latitude+' '+longitude
                    #여기서는 이제 사진 출력에 해당하는 결과 까지 다 담아서 보내야지 
                    self.__client_socket.send(mode_gps.encode())
                except Exception as e:
                    data=self.__pilot_mode.get_drone_state()+' '+str(0.00)+' '+str(0.00)
                    self.__client_socket.send(data.encode())
            except Exception as e:
                print("recvee  dead  comback 명령 실행")
                key_data=[0.0,0.0,0.0,0.0] 
                mode_data="comback"
                self.__pilot_mode.set_data(key_data,mode_data)
                print(e)
                
                
    def run(self):
        try:
            print("making thread")
            self.make_socket()
            send_thread=Thread(target=self.__data_send)
            recv_thread=Thread(target=self.__data_recv)
            send_thread.start()
            recv_thread.start()
            print("socket thread started")
        except:
            print("socket_view thread is dead")
            
    def run_camera(self):
        try:
            print("making thread")
            self.make_socket_video()
            send_thread=Thread(target=self.__data_send)
            recv_thread=Thread(target=self.__data_recv_cam)
            send_thread.start()
            recv_thread.start()
            print("socket thread started")
        except:
            print("socket_view thread is dead")
            
            
            
    def run_drone(self):
        try:
            print("making thread")
            self.make_socket_drone()
            recv_thread=Thread(target=self.__data_recv)
            recv_thread.start()
            print("socket thread started")
        except:
            print("socket_view thread is dead")
 