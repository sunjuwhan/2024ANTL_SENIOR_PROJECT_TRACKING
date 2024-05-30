import socket
import time
import sys
from threading import Thread
# A로부터 데이터를 받습니다.


# 소켓 생성


###라파 한테 받을곳 
HOST='165.229.185.195'
server_port=5000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST,server_port))  #라즈베리파이로 부터 데이터 받을 소켓이고 

#다시 vm ware로 싸줘야하는곳 
HOST_2='192.168.232.137'
PORT_2=5001
sock_2=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def recv_joystick():
    while True:
        data,addr=sock.recvfrom(1024)
        print(data)
        sock_2.sendto(data,(HOST_2,PORT_2)) #vm ware로 쏴주고





def recv_video():
    host_antl='165.229.185.195'
    prot=5002
    sock_antl = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_antl.bind((host_antl,prot))  #라즈베리파이로 부터 데이터 받을 소켓이고 
    
    while True:
        data,addr=sock_antl.recvfrom(1024)
        print("vmware로 부터 받은 데이터는 ",data)
        time.sleep(1)
        
        

thrad_a=Thread(target=recv_joystick)

thrad_b=Thread(target=recv_video)
thrad_a.start()
thrad_b.start()






