import cv2
import socket
import numpy as np
import threading

# 클라이언트 IP와 포트 설정

CLIENT_IP = '165.229.125.90'

CLIENT_PORT = 9999
ADDR = (CLIENT_IP, CLIENT_PORT)

# UDP 소켓 생성 및 바인딩
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(ADDR)

buffer = {}

def receive_video():
    while True:
        packet, _ = client_socket.recvfrom(65536)
        packet_id = packet[0]
        data = packet[1:]
        
        buffer[packet_id] = data
        
        if packet_id == 0:
            frame_data = b''.join([buffer[i] for i in sorted(buffer.keys())])
            frame = np.frombuffer(frame_data, dtype=np.uint8)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow('Received Video', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            buffer.clear()

# 영상 수신 스레드 시작
thread = threading.Thread(target=receive_video)
thread.start()

cv2.destroyAllWindows()