import spidev
import time
from drone_controller.drone_controller_information import *

class class_Drone_Controller_Joystick:
    def __init__(self, bus, device, x_channel, y_channel, switch_channel, classifyNum, ctrl_info):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 1000000
        self.x_channel = x_channel
        self.y_channel = y_channel
        self.switch_channel = switch_channel
        self.ctrl_info = ctrl_info
        self.classifyNum = classifyNum

    def read_channel(self, channel):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data
    def stabil_vrx(self,vrx_pos):
        if(vrx_pos>=485 and vrx_pos<=518):
            vrx_pos=500
        elif(vrx_pos>=0 and vrx_pos < 3):
            vrx_pos=0
        elif(vrx_pos>=1000 and vrx_pos <=1030):
            vrx_pos=1000
        return vrx_pos

    def stabil_vry(self,vry_pos):
        if(vry_pos>=485 and vry_pos<=538):
            vry_pos=500
        elif(vry_pos>=0 and vry_pos < 3):
            vry_pos=0
        elif(vry_pos>=1000 and vry_pos <=1035):
            vry_pos=1000
        return vry_pos
        
    def stabil_vrx_2(self,vrx_pos_2):
        if(vrx_pos_2>=485 and vrx_pos_2 <=535):
            vrx_pos_2=500
        elif (vrx_pos_2>=0 and vrx_pos_2 < 3):
            vrx_pos_2=0
        elif (vrx_pos_2>=1000 and vrx_pos_2<=1030):
            vrx_pos_2=1000
        return vrx_pos_2

    def stabil_vry_2(self,vry_pos_2):
        if(vry_pos_2>=490 and vry_pos_2<=520):
            vry_pos_2=500
        elif (vry_pos_2>=0 and vry_pos_2<=5):
            vry_pos_2=0
        elif (vry_pos_2>=1000 and vry_pos_2<=1030):
            vry_pos_2=1000
        return vry_pos_2 
    def read_position(self):
        x_pos = self.read_channel(self.x_channel)

        y_pos = self.read_channel(self.y_channel)
        if(self.classifyNum==1):
            y_pos =abs(y_pos-1022) 
        elif self.classifyNum==2:
            y_pos=abs(y_pos-1023) 
        switch_val = self.read_channel(self.switch_channel)
        if self.classifyNum == 1:
            self.ctrl_info.joystick_Left_x =float((self.stabil_vrx(x_pos)-500)/500)  #-1 ~ 1
            self.ctrl_info.joystick_Left_y = float((self.stabil_vry(y_pos))/1000)  
            self.ctrl_info.joystick_Left_val = switch_val
        elif self.classifyNum == 2:
            self.ctrl_info.joystick_Right_x = float((self.stabil_vrx_2(x_pos)-500)/500)
            self.ctrl_info.joystick_Right_y = float((self.stabil_vry_2(y_pos)-500)/500)
            self.ctrl_info.joystick_Right_val = switch_val
            

    def run_joystick(self):
        while True:
            self.read_position()
