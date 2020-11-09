
import socket
import threading
import sys, os

HOST = '192.168.1.2'    # The remote host
PORT = 2020          # The same port as used by the server
RECV_BUFFER=4096

def recv_data():
    while 1:
        try:
            recv_data = client_socket.recv(RECV_BUFFER).decode("utf-8")            
        except:
            #Handle the case when server process terminates
            print("Server closed connection, thread exiting.")
            sys.exit(1)
            break
        if not recv_data:
                # Recv with no data, server closed connection
                print("Server closed connection, thread exiting.")
                sys.exit(1)
                break
        else:
                print("\nReceived data: ", recv_data)

def send_data():
    "Send data from other clients connected to server"
    while 1:
        send_data = str(input("Enter data to send (q or Q to quit):"))
        send_data = send_data.encode()
        if send_data == "q" or send_data == "Q":
            client_socket.send(send_data)
            sys.exit(1)
            break
        else:
            client_socket.send(send_data)
        
if __name__ == "__main__":

    print("*******TCP/IP Chat client program********")
    print("Connecting to server at 127.0.0.1:5000")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    print("Connected to server at 127.0.0.1:5000")

    threading._start_new_thread(recv_data,())
    threading._start_new_thread(send_data,())

    try:
        while 1:
            continue
    except:
        print("Client program quits....")
        client_socket.close()        