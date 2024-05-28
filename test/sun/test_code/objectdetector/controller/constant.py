import platform
import cv2

PATH_TO_MODEL = "/home/pi/2024ANTL_SENIOR_PROJECT_TRACKING/test/sun/test_code/objectdetector/mobilenet_ssd/"
MODEL = "mobilenet_ssd_v2_coco_quant_postprocess.tflite"
TPU_MODEL = "mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite"
PATH_TO_LABEL = "/home/pi/2024ANTL_SENIOR_PROJECT_TRACKING/test/sun/test_code/objectdetector/mobilenet_ssd/coco_labels.txt"


EDGETPU = True

MIN_CONF_THRESHOLD = 0.4  # 최소값
SELECT_OBJ = "person"  # 타겟
TOP_K = 3  # 보여주는 오브젝트 갯수
FONT =cv2.FONT_HERSHEY_SIMPLEX
MIN_COUNT = 30

EDGETPU_SHARED_LIB = {
  'Linux': 'libedgetpu.so.1',
  'Darwin': 'libedgetpu.1.dylib',
  'Windows': "edgetpu.dll"
}[platform.system()]
