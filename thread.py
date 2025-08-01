import time
import threading
def first():
    time.sleep(2)
    print("from first")
def second():
    
    print("from second")
def third():
 
    print("from third")
t0 = threading.Thread(target=first)
t1 = threading.Thread(target=second)
t2 = threading.Thread(target=third)
t0.start()
t1.start()
t2.start()

t0.join()
t1.join()
t2.join()
