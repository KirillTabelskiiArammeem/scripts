import time
import threading

def dummy_func():
    while True:
        time.sleep(0.1)



for i in range(1_000_000):
    print(i)
    t = threading.Thread(target=dummy_func)
    t.start()

t.join()