from drone_controller.drone_controller_information import *
import RPi.GPIO as GPIO
import time
from threading import Thread


class class_drone_controller_button:
    def __init__(self,info:class_Drone_Controller_Information) -> None:
        self.info=info
        self.button1_pin=23
        self.button2_pin=24
        self.button3_pin=25
        self.button4_pin=17
        self.button5_pin=27
        self.button6_pin=22
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BCM) #핀모드 설정
        GPIO.setup(self.button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.button2_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.button3_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.button4_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.button5_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.button6_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
    def run_button(self):
        while True:
            if GPIO.input(self.button1_pin) == GPIO.HIGH:
                self.info.button1=(self.info.button1+1)%2
                time.sleep(0.5)      
            if GPIO.input(self.button2_pin) == GPIO.HIGH:
                self.info.button2=(self.info.button2+1)%2
                time.sleep(0.5)
            if GPIO.input(self.button3_pin) == GPIO.HIGH:
                self.info.button3=(self.info.button3+1)%2
                time.sleep(0.5)
            if GPIO.input(self.button4_pin) == GPIO.HIGH:
                self.info.button4=(self.info.button4+1)%2
                time.sleep(0.5)
            if GPIO.input(self.button5_pin) == GPIO.HIGH:
                self.info.button5=(self.info.button5+1)%2
                time.sleep(0.5)
            if GPIO.input(self.button6_pin) == GPIO.HIGH:
                self.info.button6=(self.info.button6+1)%2
                time.sleep(0.5)

 