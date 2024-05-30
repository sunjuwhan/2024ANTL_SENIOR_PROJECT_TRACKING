# import socket
# import time
# import cv2
# import numpy as np
# import socket
# import numpy
# sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# sock.bind(("192.168.50.52",8080))
# def receive_video():
#     s = [b'\xff' * 11520 for x in range(20)]

#     #fourcc = cv2.VideoWriter_fourcc(*'DIVX')
#     #out = cv2.VideoWriter('output.avi', fourcc, 25.0, (640, 480))
#     while True:
#         picture = b''
#         data, addr = sock.recvfrom(11521)
#         s[data[0]] = data[1:11521]

#         if data[0] == 19:
#             for i in range(20):
#                 picture += s[i]
#             frame = numpy.fromstring(picture, dtype=numpy.uint8)
#             frame = frame.reshape(240, 320, 3)
#             cv2.imshow("frame", frame)
#             #out.write(frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 cv2.destroyAllWindows()
#                 break
            
# receive_video()
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import socket

# UDP 설정
IP_THIS_MACHINE = "192.168.50.52"  # 수신하는 장비의 IP 주소
PORT_THIS_MACHINE = 8080  # 위에서 사용한 포트번호와 동일하게 설정
BUFFER_SIZE = 46081
video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video_socket.bind((IP_THIS_MACHINE, PORT_THIS_MACHINE))

# 이미지를 조각으로 조립하는 함수
def assemble_image(slices):
    return np.vstack(slices)

try:
    while True:
        # 이미지 조각 받기
        image_slices = []
        for i in range(20):
            data, addr = video_socket.recvfrom(BUFFER_SIZE)
            index = int.from_bytes(data[0:1], byteorder='big')  # 인덱스 추출
            image_data = np.frombuffer(data[1:], dtype=np.uint8)  # 이미지 데이터 추출
            slice_img = cv2.imdecode(image_data, cv2.IMREAD_COLOR)  # 이미지 디코딩
            image_slices.append((index, slice_img))

        # 조각을 정렬하여 이미지 조립
        image_slices.sort(key=lambda x: x[0])  # 인덱스를 기준으로 정렬
        assembled_image = assemble_image([slice_img for _, slice_img in image_slices])

        # 화면에 이미지 표시
        cv2.imshow("Received Image", assembled_image)

        # 'q' 키를 누를 때까지 대기
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # OpenCV 창 닫기 및 소켓 닫기
    cv2.destroyAllWindows()
    video_socket.close()
