import socket
import pickle
import threading
import struct
from random import seed
from random import randint

HOST = "0.0.0.0"
PORT = 2020

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created...")

s.bind((HOST, PORT))
print("Binding done...")

s.listen(5)
print("Listening for clients...")

def clientFunction(lock, clientSocket):
    winnerMessage = "You Won!"
    loserMessage = "You Lost!"
    info = clientSocket.recv(4096)
    info = pickle.loads(info)
    lock.acquire()
    if(info == number):
        clientSocket.sendall(pickle.dumps(winnerMessage))
    else:
        clientSocket.sendall(pickle.dumps(loserMessage))
    lock.release()



seed(1)
number = randint(1, 50)
lock = threading.Lock()
threads = []


while(1):
    print(number)
    c ,conn = s.accept()
    print("Connection accepted")
    t = threading.Thread(target= clientFunction, args=(lock, c,), daemon=True)
    threads.append(t)
    t.start()
s.close()
