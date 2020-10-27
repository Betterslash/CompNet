import socket
import struct
import threading

HOST = '0.0.0.0'
PORT = 2020
lock = threading.Lock()
threads = []
hangman = "HANGMAN"
trueH = list("XXXXXXX")
cuv = list("wordofcraft")
dmy = list("___________")
lives = 0

def threadFunction(con):
    global cuv, dmy, lives    
    lgt = len(cuv)
    lgt = struct.pack('!H', lgt)
    con.send(lgt)
    while True:
        mes = ""
        realH = ""
        lit = con.recv(1)
        lit = struct.unpack('!c', lit)[0].decode("utf-8")
        print("I recived ", lit)
        if lit not in cuv:
            lives += 1
            for i in range(lives):
                trueH[i] = hangman[i] 
        else:
            for i in range(len(cuv)):
                if cuv[i] == lit:
                    dmy[i] = lit
        for i in trueH:
            realH += i 
        for i in dmy:
            mes += i
        con.send(realH.encode())
        con.send(mes.encode())
    con.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created succesfully...")

s.bind((HOST, PORT))
print("Binded...")

s.listen(5)
while True:
    conn, addr = s.accept()
    print("Connection accepted...")
    t = threading.Thread(target= threadFunction, args=(conn,))
    threads.append(t)
    t.start() 
