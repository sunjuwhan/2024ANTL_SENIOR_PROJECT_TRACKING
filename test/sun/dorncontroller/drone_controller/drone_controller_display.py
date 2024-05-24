import PIL.ImageTk
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading

import time
from drone_controller.drone_controller_information import *
class class_drone_controller_display_master:
    def __init__(self, info):
        self.dc_display = None
        self.info = info


    def run_display(self):
        self.dc_display = class_drone_controller_display(self.info)



class class_drone_controller_display:
    def __init__(self, info):
        self.info = info
        self.info.display = self
        self.window = tk.Tk()
        self.window.title("Flight Controller Display")
        self.window.geometry("800x480")  # Set window size to 800x480
        self.image_id = None
        # 새로운 스레드를 생성하여 update_video 메서드를 실행합니다.
        #self.video_thread = threading.Thread(target=self.update_video_thread)
        #self.video_thread.daemon = True  # 데몬 스레드로 설정하여 메인 스레드 종료 시 함께 종료됩니다.
        #self.video_thread.start()
        # Load an example image initially
        self.info.frame = cv2.imread('/home/pi/2024ANTL_SENIO_PROJECT/img/2024_ANTL_Drone.png')

        # Convert the ndarray to PIL image
        pil_image = Image.fromarray(self.info.frame)
        resized_image = pil_image.resize((640, 480))
        # Convert the PIL image to PhotoImage
        self.vid = ImageTk.PhotoImage(resized_image)

        self.frame_canvas = tk.Canvas(self.window, width=640, height=480)
        self.frame_canvas.grid(row=0, column=0, sticky="nsew")
        self.image_id = self.frame_canvas.create_image(0, 0, image=self.vid, anchor=tk.NW)

        self.info_frame = tk.Frame(self.window, bg="#808080", width=160, height=480, bd=2, relief=tk.SOLID)  # Adjusted height for info frame
        self.info_frame.grid(row=0, column=1, sticky="nsew")

        self.gps_frame = tk.Frame(self.info_frame, bg="#404040", bd=2, relief=tk.SOLID)  # Box around GPS info
        self.gps_frame.pack(anchor="w", padx=8, pady=(4, 0), fill=tk.X)

        self.gps_label = tk.Label(self.gps_frame, text="GPS", anchor="w", bg="#404040", fg="white", font=("Arial bold", 10))  # GPS label
        self.gps_label.pack(anchor="w")

        self.latitude_label = tk.Label(self.gps_frame, text="Latitude: Waiting for data...", anchor="w",
                                       bg="#404040", fg="white",font=("Arial", 8))  # White text color
        self.latitude_label.pack(anchor="w")

        self.longitude_label = tk.Label(self.gps_frame, text="Longitude: Waiting for data...", anchor="w",
                                        bg="#404040", fg="white", font=("Arial", 8))  # White text color
        self.longitude_label.pack(anchor="w")

        self.switch_frame = tk.Frame(self.info_frame, bg="#404040", bd=2, relief=tk.SOLID)  # Box around switch info
        self.switch_frame.pack(anchor="w", padx=8, pady=(4, 0), fill=tk.X)
        switch_title = tk.Label(self.switch_frame, text="Switch", anchor="w", bg="#404040", fg="white",
                                font=("Arial bold", 10))
        switch_title.pack(anchor="w")
        self.switch_labels = []

        self.joystick_frame_L = tk.Frame(self.info_frame, bg="#404040", bd=2,
                                         relief=tk.SOLID)  # Box around joystick L info
        self.joystick_frame_L.pack(anchor="w", padx=8, pady=(4, 0), fill=tk.X)

        self.joystick_frame_R = tk.Frame(self.info_frame, bg="#404040", bd=2,
                                         relief=tk.SOLID)  # Box around joystick R info
        self.joystick_frame_R.pack(anchor="w", padx=8, pady=(4, 0), fill=tk.X)

        self.log_text_R = tk.Text(self.info_frame, width=22, height=7, bg="#1c1c1c", fg="white", font=("Arial", 8))
        self.log_text_R.pack(anchor="w", padx=8, pady=(4, 0))

        self.update_gps()
        self.update_switches()
        self.update_joystick()
        #self.update_video()
        self.window.mainloop()

    #def update_video_thread(self):
    #    while True:
    #        # update_video 메서드를 호출합니다.
    #        self.update_video()
    #        time.sleep(0.1)  # 0.1초마다 호출하도록 설정합니다.

    def update_video(self, frame):
        #frame = self.info.frame
        new_img = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        #pil_image = Image.fromarray(frame)

        # PIL 이미지를 PhotoImage로 변환
        #new_img = ImageTk.PhotoImage(image=pil_image)
        #self.frame_canvas.create_image(0, 0, image=new_img, anchor=tk.NW)
        self.frame_canvas.itemconfig(self.image_id,image=new_img)
        #self.window.after(10, self.update_video)

    def update_switches(self):
        for label in self.switch_labels:
            label.destroy()

        self.switch_labels = []
        for i in range(1, 5):  # 1부터 4까지 반복
            switch_value = getattr(self.info, f'switch{i}')  # self.info.switch1, self.info.switch2 등을 가져옴
            switch_label = tk.Label(self.switch_frame, text=f"Switch {i}: {switch_value}",
                                    anchor="w", bg="#404040", fg="white", font=("Arial", 8))  # White text color
            switch_label.pack(anchor="w", padx=8)
            self.switch_labels.append(switch_label)
        self.window.after(500, self.update_switches)

    def update_gps(self):
        latitude_text = f"Latitude: {self.info.drone_latitude:.5f}"
        longitude_text = f"Longitude: {self.info.drone_longitude:.5f}"

        self.latitude_label.config(text=latitude_text)
        self.longitude_label.config(text=longitude_text)
        self.window.after(2000, self.update_gps)

    def update_joystick(self):
        # Simulate joystick data
        joystick_values_L = {
            'x': self.info.joystick_Left_x,
            'y': self.info.joystick_Left_y,
            'switch': self.info.joystick_Left_val
        }
        joystick_values_R = {
            'x': self.info.joystick_Right_x,
            'y': self.info.joystick_Right_y,
            'switch': self.info.joystick_Right_val
        }

        self.update_joystick_labels(self.joystick_frame_L, "Joystick L", joystick_values_L)
        self.update_joystick_labels(self.joystick_frame_R, "Joystick R", joystick_values_R)
        self.window.after(300, self.update_joystick)

    def update_joystick_labels(self, frame, name, values):
        for label in frame.winfo_children():
            label.destroy()

        joystick_label = tk.Label(frame, text=name, anchor="w", bg="#404040", fg="white", font=("Arial bold", 10))
        joystick_label.pack(anchor="w")

        x_label = tk.Label(frame, text=f"x: {values['x']}", anchor="w", bg="#404040", fg="white", font=("Arial", 8))
        x_label.pack(anchor="w", padx=(8, 0))

        y_label = tk.Label(frame, text=f"y: {values['y']}", anchor="w", bg="#404040", fg="white", font=("Arial", 8))
        y_label.pack(anchor="w", padx=(8, 0))

        switch_label = tk.Label(frame, text=f"switch: {'ON' if values['switch'] else 'OFF'}", anchor="w",
                                bg="#404040", fg="white", font=("Arial", 8))
        switch_label.pack(anchor="w", padx=(8, 0))




if __name__ == "__main__":
    dc_display = class_drone_controller_display(class_Drone_Controller_Information())