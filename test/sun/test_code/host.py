import socket
import time
import sys

# A로부터 데이터를 받습니다.


# 소켓 생성



#HOST='165.229.185.195'
server_port=8080
HOST='192.168.50.71'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST,server_port))
sock.listen(1)
client_sock,addr=sock.accept()  #cline_sock은 이제 컨트롤러에서 내 pc로 전송할 데이터이고


print("accept end")
HOST_2='192.168.232.138'
PORT_2=8000

sock_2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #이친구는 이제 내 PC에서 VMWARE로 데이터 전송
print("wait connect")
sock_2.connect((HOST_2,PORT_2))
print("end connetc")
while True:
    data,addr=client_sock.recvfrom(100) #컨트롤러에서 받아서
    sock_2.sendto(data,(HOST_2,PORT_2))  #VMWARE로 쏴주고
    
    
    
    recv_data=sock_2.recv(100).decode().split(' ')
    
    
    
    arm_data=recv_data[0]
    print(data)
    client_sock.send(arm_data.encode())