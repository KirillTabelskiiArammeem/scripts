import threading
import time
import multiprocessing


def foo():
    while True:
        time.sleep(5)


def thread_fabric(x):
    i = 0
    while True:
        i += 1
        threading.Thread(target=foo).start()
        print(x, i)


def main():
    processes = [multiprocessing.Process(target=thread_fabric, args=(x,)) for x in range(10)]
    [p.start() for p in processes]
    [p.join() for p in processes]


main()
