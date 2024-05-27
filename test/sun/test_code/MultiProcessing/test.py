from multiprocessing import Pool
import os
import time 
def function_A():
    print(f"Function A is running in process ID: {os.getpid()}")
    # A 함수의 작업을 여기에 추가하세요.
    i=0
    while True:
        i+=1
        print(f"Function A: {i}")
        time.sleep(0.1)

def function_B():
    print(f"Function B is running in process ID: {os.getpid()}")
    # B 함수의 작업을 여기에 추가하세요.
    while True:
        print(f"Function B:")
        time.sleep(1)

if __name__ == "__main__":
    with Pool(processes=2) as pool:  # 2개의 프로세스로 풀을 만듭니다.
        result_A = pool.apply_async(function_A)
        result_B = pool.apply_async(function_B)

        # 결과를 기다립니다.
        result_A.wait()
        result_B.wait()

    print("Both processes have finished execution.")
