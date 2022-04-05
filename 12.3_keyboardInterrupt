import threading
import time

sem = threading.Semaphore()
STOP_FLAG = True

def fun1():
    global STOP_FLAG
    try:
        while STOP_FLAG:
            sem.acquire()
            print(1, end='')
            sem.release()
            time.sleep(0.25)
    except KeyboardInterrupt:
        STOP_FLAG = False


def fun2():
    global STOP_FLAG
    try:
        while STOP_FLAG:
            sem.acquire()
            print(2, end='')
            sem.release()
            time.sleep(0.25)
    except KeyboardInterrupt:
        STOP_FLAG = False


if __name__ == '__main__':
    t1 = threading.Thread(target=fun1)
    t1.start()
    t2 = threading.Thread(target=fun2)
    t2.start()
