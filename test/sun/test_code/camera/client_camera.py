import socket
import cv2
import time
import numpy as np
from picamera2 import Picamera2
UDP_IP = "192.168.50.15"
UDP_PORT = 8005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# 카메라 해상도 설정
picam2 = Picamera2()
picam2.preview_configuration.main.size = (320, 240)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()
while True:
    frame = picam2.capture_array()
    # 프레임을 JPEG 형식으로 압축
    _, encoded_frame = cv2.imencode('.jpg', frame)
    
    # 압축된 이미지 데이터를 바이트 스트링으로 변환
    s = encoded_frame.tobytes()

    # 바이트 스트링을 여러 패킷으로 나누어 전송
    for i in range(5):
        sock.sendto(bytes([i]) + s[i * 46080:(i + 1) * 46080], (UDP_IP, UDP_PORT))  # JPEG 압축된 프레임 전송


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
