import socket
import time
import threading

#Global Variables
COptionFile = open("COptionFile.txt", "r")
serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 1024
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Handshake
UDPClientSocket.sendto(str.encode("Clientrec"), serverAddressPort)
bytesFromServer = UDPClientSocket.recvfrom(bufferSize)
if bytesFromServer[0] == str.encode("Serveracc"):
    UDPClientSocket.sendto(str.encode("Clientacc"), serverAddressPort)

def clientChat(UDPClientSocket):
    while True:
            msgFromClient = input("Client: ")
            bytesToSend = str.encode(msgFromClient)
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)
            time.sleep(0.1)
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
            if msgFromServer[0] == bytes(0xFE):
                UDPClientSocket.sendto(bytes(0xFF), serverAddressPort)
                UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                UDPClientSocket.sendto(bytes(0xF1), serverAddressPort)
                bytesFromServer = UDPClientSocket.recvfrom(bufferSize)
                if bytesFromServer[0] == bytes(0xF2):
                    UDPClientSocket.sendto(bytes(0xF3), serverAddressPort)
            else:
                msg = "Message from Server {}".format(msgFromServer[0])
                print(msg)

def keepAlive():
    while True:
        autoMsg = bytes(0x00)
        UDPClientSocket.sendto(autoMsg, serverAddressPort)
        time.sleep(3)


#seperate thread for keepAlive function
keepAliveThread = threading.Thread(name="keepAlive", target=keepAlive)


if COptionFile.read() == "True":
    keepAliveThread.start()
clientChat(UDPClientSocket)

