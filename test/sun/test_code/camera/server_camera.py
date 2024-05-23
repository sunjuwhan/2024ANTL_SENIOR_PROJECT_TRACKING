import socket
import numpy as np
import cv2
import time

UDP_IP = "192.168.50.15"
UDP_PORT = 9505

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# 각 프레임의 바이트 스트링을 저장할 리스트
frames = [b'' for _ in range(5)]

while True:
    picture = b''
    data, addr = sock.recvfrom(46081)  # 각 패킷은 46081바이트
    frames[data[0]] = data[1:46081]  # 수신된 프레임 데이터 저장
    if data[0] == 4:  # 모든 패킷을 다 받았을 때
        for i in range(5):
            picture += frames[i]  # 모든 프레임 데이터를 하나로 합침

        # 바이트 스트링을 numpy 배열로 변환하고 이미지로 디코딩
        frame = cv2.imdecode(np.frombuffer(picture, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow("frame", frame)

        # 프레임 표시 시간 계산

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
