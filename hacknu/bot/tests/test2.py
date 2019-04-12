from client import Client
import threading

print("started")
cl = Client()

def SMTH(state):
    print(str(a)+"     " + str(cl.GetAllBooks()))

    return


a = 0
while a<5:
    a += 1
    my_thread = threading.Thread(target=SMTH, args={a,})
    my_thread.start()
    