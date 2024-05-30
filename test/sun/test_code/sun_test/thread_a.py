from threading import Thread
import time
def run_a():
    while True:
        print('ad')
        time.sleep(4)
        
thread_a=Thread(target=run_a)
thread_a.start()

print("adsfadfasdf")