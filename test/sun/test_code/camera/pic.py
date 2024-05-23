"""
* Project : 2023CDP camera module 3 test file
* Program Purpose and Features :
* - amera module 3 test
* Author : JH KIM
* First Write Date : 2023.08.24
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		Version		History
* JH KIM            2023.08.24		v1.00		First Write
"""

import cv2
from picamera2 import Picamera2

picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280,720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()
while True:
    im= picam2.capture_array()
    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Camera", grey)
    picam2.stop()
    