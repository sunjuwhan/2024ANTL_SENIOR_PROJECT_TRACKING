import spidev
import time


class class_Drone_Controller_Joystick:
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 1000000
        self.x_channel = 1
        self.y_channel = 2
        self.switch_channel = 0


    def read_channel(self, channel):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data


    def read_position(self):
        x_pos = self.read_channel(self.x_channel)
        y_pos = self.read_channel(self.y_channel)
        switch_val = self.read_channel(self.switch_channel)
        print("x: {}, y: {}, sw:{}".format(x_pos,y_pos,switch_val))

if __name__=="__main__":
    dc_joystick = class_Drone_Controller_Joystick()
    while True:
        dc_joystick.read_position()