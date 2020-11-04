import socket
import struct
import threading
import sys
import time
from copy import deepcopy
from random import randint
from termcolor import colored

HOST = "0.0.0.0"
PORT = 2020
threads = []
lock = threading.Lock()
tableRepre = [['  \\', ' A', ' B', ' C', ' D', ' E', ' F', ' G', ' H', ' I', ' J'],
              [' 1 ', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],
              [' 2 ', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],
              [' 3 ', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],
              [' 4 ', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],
              [' 5 ', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],
              [' 6 ', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],
              [' 7 ', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],
              [' 8 ', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],
              [' 9 ', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],
              ['10 ', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛']]
headsList = []


def representationToString(table):
    rep = ""
    for i in range(11):
        for j in range(11):
            rep += table[i][j]
        rep += '\n'
    return rep


def generatePlanes():
    table = deepcopy(tableRepre[:])
    while str(table).count('⬜') < 30:
        positionX = randint(3, 6)
        positionY = randint(3, 6)
        head1 = [positionX, positionY]
        for i in range(4):
            table[positionX][positionY + i] = colored("⬜", 'blue')
        for i in range(-2, 3):
            table[positionX + i][positionY + 1] = colored("⬜", 'blue')
        for i in range(-1, 2):
            table[positionX + i][positionY + 3] = colored("⬜", 'blue')
        psX = randint(3, 6)
        psY = randint(3, 6)
        head2 = [psX, psY]
        for i in range(4):
            table[psX + i][psY] = colored("⬜", 'red')
        for i in range(-2, 3):
            table[psX + 1][psY + i] = colored("⬜", 'red')
        for i in range(-1, 2):
            table[psX + 3][psY + i] = colored("⬜", 'red')
        posX = randint(3, 6)
        posY = randint(6, 10)
        head3 = [posX, posY]
        for i in range(4):
            table[posX][posY - i] = colored("⬜", 'green')
        for i in range(-2, 3):
            table[posX - i][posY - 1] = colored("⬜", 'green')
        for i in range(-1, 2):
            table[posX - i][posY - 3] = colored("⬜", 'green')
        if str(table).count('⬜') == 30:
            global headsList
            headsList = [head1, head2, head3]
            return [table, headsList]
        table.clear()
        table = deepcopy(tableRepre[:])


def shoot(ps, tables, lives):
    orient = -1
    for i in range(3):
        if ps == tables[1][i]:
            orient = i
    if orient == 0:
        for i in range(4):
            tables[0][tables[1][orient][0]][tables[1][orient][1] + i] = colored("⛝", 'blue')
        for i in range(-2, 3):
            tables[0][tables[1][orient][0] + i][tables[1][orient][1] + 1] = colored("⛝", 'blue')
        for i in range(-1, 2):
            tables[0][tables[1][orient][0] + i][tables[1][orient][1] + 3] = colored("⛝", 'blue')
        lives -= 10
    elif orient == 1:
        for i in range(4):
            tables[0][tables[1][orient][0] + i][tables[1][orient][1]] = colored("⛝", 'red')
        for i in range(-2, 3):
            tables[0][tables[1][orient][0] + 1][tables[1][orient][1] + i] = colored("⛝", 'red')
        for i in range(-1, 2):
            tables[0][tables[1][orient][0] + 3][tables[1][orient][1] + i] = colored("⛝", 'red')
        lives -= 10
    elif orient == 2:
        for i in range(4):
            tables[0][tables[1][orient][0]][tables[1][orient][1] - i] = colored("⛝", 'green')
        for i in range(-2, 3):
            tables[0][tables[1][orient][0] - i][tables[1][orient][1] - 1] = colored("⛝", 'green')
        for i in range(-1, 2):
            tables[0][tables[1][orient][0] - i][tables[1][orient][1] - 3] = colored("⛝", 'green')
        lives -= 10
    else:
        if tables[0][ps[0]][ps[1]] == colored("⬜", 'green') or tables[0][ps[0]][ps[1]] == colored("⬜", 'blue') or \
                tables[0][ps[0]][ps[1]] == colored("⬜", 'red'):
            tables[0][ps[0]][ps[1]] = '⛝'
            lives -= 1
        else:
            tables[0][ps[0]][ps[1]] = '⬜'
    return lives


def serverShoot(tables, lives):
    p = [-1, -1]
    p[0] = randint(1, 10)
    p[1] = randint(1, 10)
    while tables[0][p[0]][p[1]] == '⬜' or tables[0][p[0]][p[1]] == '⛝':
        p[0] = randint(1, 10)
        p[1] = randint(1, 10)
    lives = shoot(p, tables, lives)
    return lives


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created...")
s.bind((HOST, PORT))
print("Socket binded")
s.listen(5)
print("Listening for connections...")


def threadFunction(co):
    client = generatePlanes()
    clientTable = client[0]
    server = generatePlanes()
    serverTable = server[0]
    serverLives = 30
    playerLives = 30
    print(representationToString(clientTable))
    while playerLives > 0 and serverLives > 0:
        print(representationToString(serverTable))
        x = co.recv(2)
        x = struct.unpack('!H', x)[0]
        y = co.recv(2)
        y = struct.unpack('!H', y)[0]
        shp = [x, y]
        serverLives = shoot(shp, server, serverLives)
        playerLives = serverShoot(client, playerLives)
        mes = maskMap(serverTable)
        lock.acquire()
        lgt = sys.getsizeof(mes)
        lgt = struct.pack('!H', lgt)
        co.send(lgt)
        co.send(mes.encode())
        time.sleep(0.25)
        if playerLives <= 0:
            m = 'L'
            co.send(m.encode())
            print("I won!")
            lock.release()
            return
        elif serverLives <= 0:
            m = 'W'
            co.send(m.encode())
            print("I lost!")
            lock.release()
            return
        else:
            co.send(b'm')
        print('Player lives are', playerLives)
        print('Server lives are', serverLives)
        lock.release()
    co.close()


def maskMap(table):
    s = ''
    for i in range(11):
        for j in range(11):
            if table[i][j] == colored("⬜", 'red') or table[i][j] == colored("⬜", 'green') or table[i][j] == colored("⬜",'blue'):
                s += '⬛' + ' '
            elif table[i][j] == colored("⛝", 'green') or table[i][j] == colored("⛝", 'blue') or table[i][j] == colored(
                    "⛝", 'red') or table[i][j] == "⛝":
                s += '➕' + ' '
            else:
                s += table[i][j] + ' '
        s += '\n'
    return s


while True:
    c, addr = s.accept()
    t = threading.Thread(target=threadFunction, args=(c,))
    threads.append(t)
    t.start()
