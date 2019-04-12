import threading
from client import Client as cl
import time
import os

def _timer(number):
    print("timer started")
    time.sleep(60)
    with open(os.getcwd()+"\\test.txt","w") as file:
        file.write("1")
    print("timer stopped")
    

    return
 
def worker(number):
    print("worker started")
    a = 0
    while a<10000:
        if os.path.exists(os.getcwd()+"\\test.txt"):
            break
        cli = cl
        print(str(number) +": "+ str(cli.CreateUser(int(a),"test","@test"+str(a))))
        a = a + 1
    print(a)

    return


print("starting new thread....")
my_thread = threading.Thread(target=_timer, args=(1,))
my_thread.start()

a = 0
while a < 100:
    print("starting new thread...." + str(a))
    my_thread = threading.Thread(target=worker, args=(a,))
    my_thread.start()

