import socket, pickle

def sumOfElements(arr):
    sum = 0
    for x in arr:
        sum += x
    return pickle.dumps(sum)
def countOfSpaces(strg):
    count = 0
    for s in strg:
        if s == " ":
            count += 1
    return pickle.dumps(count)

HOST = '0.0.0.0'
PORT = 3030
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(2)
conn, addr = s.accept()
print('Connected by')
print(addr)
while 1:
    data = conn.recv(4096)
    #if not data: break
    print(pickle.loads(data))
    msg = str(input("Text >>"))
    data_text = pickle.dumps(msg)
    conn.send(data_text)
conn.close()