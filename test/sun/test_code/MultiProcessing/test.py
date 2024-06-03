from multiprocessing import Pool, Manager
import os
import time

def function_A(shared_data):
    print(f"Function A is running in process ID: {os.getpid()}")
    # A 함수의 작업을 여기에 추가하세요.
    while True:
        if 'key' in shared_data:
            print(f"Function A: {shared_data['key']}")
        else:
            print("Function A: key not found")
        time.sleep(0.7)

def function_B(shared_data):
    print(f"Function B is running in process ID: {os.getpid()}")
    # B 함수의 작업을 여기에 추가하세요.
    i = 0
    while True:
        shared_data['key'] = i
        print(f"Function B: setting key to {i}")
        i += 1
        time.sleep(1)

if __name__ == "__main__":
    with Manager() as manager:
        shared_data = manager.dict()

        with Pool(2) as p:
            result_A = p.apply_async(function_A, (shared_data,))
            result_B = p.apply_async(function_B, (shared_data,))

            # 결과를 기다립니다.
            p.close()
            p.join()

    print("Both processes have finished execution.")
