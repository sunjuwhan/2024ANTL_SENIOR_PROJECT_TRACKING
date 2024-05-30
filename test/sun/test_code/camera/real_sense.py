import cv2
import numpy as np
import pyrealsense2.pyrealsense2 as rs






pipeline = rs.pipeline()  # intel realsense capture
config = rs.config()  # intel realsense configuration

pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

        # RGB & Depth
#config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
raw_frame=None

while True:
    frames =pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    raw_frame=np.asanyarray(color_frame.get_data())
    cv2.imshow(raw_frame)