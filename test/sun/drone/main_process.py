from multiprocessing import Pool
from main_camera import *
from main import *
import os

if __name__ == "__main__":
    with Pool(processes=2) as pool:  # 2개의 프로세스로 풀을 만듭니다.
        print("Start Multi Processing Drone")
        main_camera=MainCamera()
        main_drone=MainDrone()
        result_A = pool.apply_async(main_camera.run)
        result_B = pool.apply_async(main_drone.run_drone_main)
        # 결과를 기다립니다.
        result_A.wait()
        result_B.wait()
    print("now")

