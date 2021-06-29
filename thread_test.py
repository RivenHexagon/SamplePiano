import time
import threading

def thrdel(name, dly):
    cnt = 0
    while cnt < 4:
        time.sleep(dly)
        cnt += 1
        print(name, '--->', time.time())

def playSound(_title):
    print(_title)

if __name__ == '__main__':
    t1 = threading.Thread( target=thrdel, args=('t1',1) )
    t2 = threading.Thread( target=thrdel, args=('t2',2) )
    t3 = threading.Thread( target=playSound, args=('t2',) )

    t1.start()
    t2.start()
    t3.start()
    t2.join()
    print("t2 done")    
    t1.join()
    print("t1 done")


''' END '''

