class class_Drone_Controller_Information:
    def __init__(self):
        self.joystick_Left_x = 0
        self.joystick_Left_y = 0
        self.joystick_Left_val = 0
        self.joystick_Right_x = 0
        self.joystick_Right_y = 0
        self.joystick_Right_val = 0
        self.button1=0
        self.button2=0
        self.button3=0
        self.button4=0
        self.button5=0
        self.button6=0
        self.switch1 = 0
        self.switch2 = 0
        self.switch3 = 0
        self.switch4 = 0
        self.drone_state="disarm"
        self.arr_switch = [self.switch1, self.switch2, self.switch3, self.switch4]
        self.joystick_data=" "
        self.arm_data="disarm"
        self.frame=None
        self.drone_latitude = 35.830622286686854
        self.drone_longitude = 128.7544099722211
        self.now_mode="manual"
        self.display = None