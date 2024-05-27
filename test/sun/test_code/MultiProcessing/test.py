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
    p=Pool(2)
    result_A = p.apply_async(function_A,)
    result_B = p.apply_async(function_B,)

    # 결과를 기다립니다.
    p.close()
    p.join()

    print("Both processes have finished execution.")
