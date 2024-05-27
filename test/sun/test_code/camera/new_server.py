# import cv2
# import socket
# import struct
# import threading

from picamera2 import Picamera2

# # 서버 IP와 포트 설정
# SERVER_IP = '192.168.32.3'
# SERVER_PORT = 9999
# ADDR = (SERVER_IP, SERVER_PORT)

# # UDP 소켓 생성
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# def send_video():
#     picam2=Picamera2()
#     picam2.preview_configuration.main.size = (640, 480)
#     picam2.preview_configuration.main.format = "RGB888"
#     picam2.preview_configuration.align()
#     picam2.configure("preview")
#     picam2.start()
#     frame_id = 0

#     while True:
#         frame=picam2.capture_array()
#         # 프레임을 JPEG 형식으로 압축 (디폴트 품질 설정: 95)
#         _, buffer = cv2.imencode('.jpg', frame)
#         data = buffer.tobytes()
        
#         # 프레임을 청크로 분할하여 전송
#         packet_size = 65507 - 10  # UDP 패킷 최대 크기 (프레임 ID와 패킷 ID를 위해 3 바이트 제외)
#         num_packets = len(data) // packet_size + (1 if len(data) % packet_size != 0 else 0)

#         for i in range(num_packets):
#             packet_data = data[i*packet_size:(i+1)*packet_size]
#             packet = struct.pack("BH", i, frame_id) + packet_data
#             server_socket.sendto(packet, ADDR)
        
#         frame_id = (frame_id + 1) % 65527  # 프레임 ID는 0-65535 범위를 유지

#     cap.release()

# # 영상 전송 스레드 시작
# thread = threading.Thread(target=send_video)
# thread.start()



import cv2
import socket
import struct
import threading
import time


# 서버 IP와 포트 설정

SERVER_IP = '192.168.32.1'
SERVER_PORT = 9999
ADDR = (SERVER_IP, SERVER_PORT)

# UDP 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_video():
    picam2=Picamera2()
    picam2.preview_configuration.main.size = (640, 480)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()
    frame_id = 0
    while True:
        frame=picam2.capture_array()
        
        # 프레임을 JPEG 형식으로 압축
        _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        data = buffer.tobytes()
        
        # 프레임을 청크로 분할하여 전송

        packet_size = 65507  # UDP 패킷 최대 크기

        num_packets = len(data) // packet_size + (1 if len(data) % packet_size != 0 else 0)

        for i in range(num_packets):
            packet_data = data[i*packet_size:(i+1)*packet_size]
            server_socket.sendto(struct.pack("B", i) + packet_data, ADDR)
            time.sleep(0.001)  # 패킷 사이의 작은 지연 추가

    cap.release()

# 영상 전송 스레드 시작
thread = threading.Thread(target=send_video)
thread.start()