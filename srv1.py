
import socket               # Import socket module
import threading
import pickle
import os
import subprocess
from subprocess import PIPE, Popen
def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

def on_new_client(lock ,clientsocket, addr, i):
    data_file_path = 'file' + str(i) +'.txt'
    msg = clientsocket.recv(4096)
        #do some checks and if msg == someWeirdSignal: break:
    mtx = pickle.loads(msg)
    lock.acquire()
    os.system("stat -c %s t " + mtx + '>' + data_file_path)
    os.system("cat " + mtx + ">>" + data_file_path)
    with open(data_file_path, 'r') as file:
        datas = file.read()
        file.close()
    os.remove(data_file_path)
    lock.release()
    print(datas)
        #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
    if datas == "":
        clientsocket.send(pickle.dumps(-1))    
    else:
        clientsocket.send(pickle.dumps(datas))
    clientsocket.close()



s = socket.socket()         # Create a socket object
#host = socket.gethostname() # Get local machine name
port = 3030                # Reserve a port for your service.

print('Server started!')
print('Waiting for clients...')

s.bind(("0.0.0.0", port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.

print('Got connection from') 
i = 0
threads = []
while True:
   i += 1
   c, addr = s.accept()
   lock = threading.Lock()
   t = threading.Thread(target = on_new_client,args=(lock,c,addr,i,))
   threads.append(t)
   t.start()
   #Note it's (addr,) not (addr) because second parameter is a tuple
   #Edit: (c,addr)
   #that's how you pass arguments to functions when creating new threads using thread module.
for i in range(0, len(threads) - 1):
    threads[i].join()
s.close()
