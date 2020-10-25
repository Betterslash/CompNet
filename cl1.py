import struct
import socket

HOST = "192.168.1.2"
PORT = 2020

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

arr = []
l = len(arr)

l = struct.pack('!H', l)
s.send(l)

for i in range(0, len(arr)):
    el = struct.pack('!H', arr[i])
    s.send(el)

lg = s.recv(2)
lg = struct.unpack('!H',lg)[0]
print(lg)
sir = []
for i in range(0, lg - 1):
    el = s.recv(2)
    el = struct.unpack('!H', el)[0]
    sir.append(el)
print(sir)
