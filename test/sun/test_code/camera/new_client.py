import cv2
import socket
import numpy as np
import threading
import collections
import struct
# 클라이언트 IP와 포트 설정
CLIENT_IP = '165.229.125.90'
CLIENT_PORT = 9999
ADDR = (CLIENT_IP, CLIENT_PORT)

# UDP 소켓 생성 및 바인딩
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(ADDR)

buffer = collections.defaultdict(lambda: [None] * 256)
expected_frame_id = 0

def receive_video():
    global expected_frame_id

    while True:
        packet, _ = client_socket.recvfrom(65536)
        packet_id, frame_id = struct.unpack("BH", packet[:3])
        data = packet[3:]
        
        if frame_id == expected_frame_id:
            buffer[frame_id][packet_id] = data

            if None not in buffer[frame_id]:
                frame_data = b''.join(buffer[frame_id])
                frame = np.frombuffer(frame_data, dtype=np.uint8)
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                if frame is not None:
                    cv2.imshow('Received Video', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                del buffer[frame_id]
                expected_frame_id = (expected_frame_id + 1) % 65536

# 영상 수신 스레드 시작
thread = threading.Thread(target=receive_video)
thread.start()

cv2.destroyAllWindows()
