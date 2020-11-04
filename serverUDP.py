import socket
import struct


def addArrayToArray(clientArr):
    global arr
    for siz in range(len(clientArr)):
        arr.append(clientArr[siz])
    return clientArr


def merge_sort(values):
    if len(values) > 1:
        m = len(values) // 2
        left = values[:m]
        right = values[m:]
        left = merge_sort(left)
        right = merge_sort(right)
        values = []
        while len(left) > 0 and len(right) > 0:
            if left[0] < right[0]:
                values.append(left[0])
                left.pop(0)
            else:
                values.append(right[0])
                right.pop(0)
        for val in left:
            values.append(val)
        for val in right:
            values.append(val)
    return values


arr = []
PORT = 2020
HOST = '0.0.0.0'
paramTuple = (HOST, PORT)
adresses = []


def sendIntToAll(sock, nmb):
    global adresses
    for adr in adresses:
        sock.sendto(nmb, adr)


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
print("Socket created...")
s.bind((HOST, PORT))
print("Socket binded...")

while True:
    lgt, clData = s.recvfrom(2)
    lgt = struct.unpack('!H', lgt)[0]
    adresses.append(clData)
    for i in range(lgt):
        elem, clData = s.recvfrom(2)
        elem = struct.unpack('!H', elem)[0]
        arr.append(elem)
    print("I have ", arr, "with recived length of ", lgt, "!")
    if lgt == 0:
        print("Now i stopped !")
        arr = merge_sort(arr)
        lgt = len(arr)
        lgt = struct.pack('!H', lgt)
        sendIntToAll(s, lgt)
        for el in arr:
            el = struct.pack('!H', el)
            sendIntToAll(s, el)
        break


s.close()
