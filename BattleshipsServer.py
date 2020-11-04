import socket
import struct
import threading
from random import randint

HOST = '0.0.0.0'
PORT = 2020

threads = []
lock = threading.Lock()


def threadFunction(cone):
    serverLife = 7
    playerLife = 7
    playerBoard = generateShips()
    print(displayTable(playerBoard))
    serverBoard = generateShips()
    print(displayTable(serverBoard))
    move = [0,0]
    while serverLife > 0 and playerLife > 0:
        move[0] = cone.recv(2)
        move[0] = struct.unpack('!H', move[0])[0]
        move[1] = cone.recv(2)
        move[1] = struct.unpack('!H', move[1])[0]
        shoot(move, serverBoard, serverLife)
        if serverLife == 0:
            print("I lost!...")
            return
        serverShoot(playerBoard, playerLife)
        if playerLife == 0:
            print("I won!...")
            return
        mes = maskBoard(serverBoard)
        cone.send(struct.pack('!H', playerLife))
        cone.send(mes.encode())
    cone.close()


def displayTable(b):
    srepr = ""
    for i in range(11):
        for j in range(10):
            srepr += b[i][j] + " "
        srepr += '\n'
    return srepr


def generateShips():
    gt = [[" \\", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
          [" 1", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*"],
          [" 2", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*"],
          [" 3", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*"],
          [" 4", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*"],
          [" 5", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*"],
          [" 6", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*"],
          [" 7", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*"],
          [" 8", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*"],
          [" 9", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*"],
          ["10", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*"]]
    sedX = randint(1, 7)
    for i in range(sedX, sedX + 3):
        gt[sedX][i] = "T"
    sedY = randint(1, 7)
    while sedY - 3 <= sedX <= sedY:
        sedY = randint(1, 7)
    for i in range(sedX, sedX + 4):
        gt[i][sedY] = "T"
    return gt


def shoot(pos, board, life):
    if board[pos[0]][pos[1]] == "T":
        board[pos[0]][pos[1]] = "X"
        life -= 1
    else:
        board[pos[0]][pos[1]] = "O"


def serverShoot(playerBoard, playerLife):
    pos = [randint(1, 10), randint(1, 10)]
    while playerBoard[pos[0]][pos[1]] == "X":
        pos = [randint(1, 10), randint(1, 10)]
    shoot(pos, playerBoard, playerLife)
    print(displayTable(playerBoard))


def playerShoot(pos, serverT, serverLife):
    shoot(pos, serverT, serverLife)


def maskBoard(serverT):
    reps = ""
    for i in range(11):
        for j in range(11):
            if serverT[i][j] == "T":
                reps += "* "
            else:
                reps += serverT[i][j] + " "
        reps += '\n'
    return reps


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket connected...")
s.bind((HOST, PORT))
print("Socket binded...")
s.listen(5)
print("Listening...")

while True:
    co, adro = s.accept()
    print("I recived the connection...")
    print("The Game just begun...")
    t = threading.Thread(target=threadFunction, args=(co,))
    threads.append(t)
    t.start()
