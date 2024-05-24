import cv2
from picamera2 import Picamera2
import numpy as np

# Picamera2 객체 생성
picam2 = Picamera2()

# 카메라 설정 구성
config = picam2.create_preview_configuration()
picam2.configure(config)

# 카메라 시작
picam2.start()

while True:
    # 이미지를 numpy 배열로 캡처
    frame = picam2.capture_array()

    # OpenCV를 사용하여 이미지 표시
    cv2.imshow("Camera Frame", frame)

    # 'q' 키를 누르면 루프 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 카메라 종료
picam2.stop()

# OpenCV 윈도우 종료
cv2.destroyAllWindows()
