import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading
import time

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

        self.info.frame = cv2.imread('/home/pi/2024ANTL_SENIO_PROJECT/img/2024_ANTL_Drone.png')

        pil_image = Image.fromarray(self.info.frame)
        resized_image = pil_image.resize((640, 480))
        self.vid = ImageTk.PhotoImage(resized_image)

        self.image_label = tk.Label(self.window, image=self.vid)
        self.image_label.grid(row=0, column=0, sticky="nsew")

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

        self.drone_state_frame = tk.Frame(self.info_frame, bg="#404040", bd=2,
                                          relief=tk.SOLID)  # Box around drone state
        self.drone_state_frame.pack(anchor="w", padx=8, pady=(4, 0), fill=tk.X)

        self.drone_state_title = tk.Label(self.drone_state_frame, text="Drone State", anchor="w", bg="#404040",
                                          fg="white", font=("Arial bold", 10))
        self.drone_state_title.pack(anchor="w")

        self.drone_state_label = tk.Label(self.drone_state_frame, text="Waiting for data...", anchor="w", bg="#404040",
                                          fg="white", font=("Arial", 8))
        self.drone_state_label.pack(anchor="w")

        self.update_gps()
        self.update_switches()
        self.update_joystick()
        self.window.mainloop()

    def update_video(self, frame):
        new_img = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.image_label.configure(image=new_img)
        self.image_label.image = new_img

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

    def update_drone_state(self):
        drone_state_text = f"Arm Data: {self.info.arm_data}"
        self.drone_state_label.config(text=drone_state_text)