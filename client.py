import socket
import pickle

HOST = '127.0.0.1'
PORT = 5000

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))

message = "Hi there master"
data = pickle.dumps(message)
s.send(data)


recived = s.recv(4096)
s.close()
print(pickle.loads(recived))

