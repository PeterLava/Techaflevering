import socket
import sys
import time
from datetime import date
from datetime import datetime

#Global Variables
today = datetime.now()
todaysDate = today.strftime("%d/%m/%Y %H:%M:%S")
msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)
bufferSize = 1024
localIP = "127.0.0.1"
localPort = 20001
SOptionFile = open("SOptionFile.txt", "r")
ammPck = 1/int(SOptionFile.read())

#Socket
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")


def chat(message, address):
    i = 1
    while (True):
        UDPServerSocket.settimeout(4)
        try:
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
        except socket.timeout:
            print("Too slow...")
            try:
                UDPServerSocket.sendto(bytes(0xFE), address)
                print("UDP server up and listening")
                break
            except:
                print("UDP server up and listening")
                break

        clientMsg = "C: com-" + i + " Message: {}".format(message)
        clientIP = "Client IP Address:{}".format(address)
        print(clientMsg)
        print(clientIP)
        UDPServerSocket.sendto(bytesToSend, address)
        time.sleep(ammPck)
        i = i + 1
#MAIN
while True:
    try:
        #Handshake
        bytesFromClient = UDPServerSocket.recvfrom(bufferSize)
        message = bytesFromClient[0]
        address = bytesFromClient[1]
        if bytesFromClient[0] == str.encode("Clientrec"):
            print("C: com-0", bytesFromClient[1])
            UDPServerSocket.sendto(str.encode("Serveracc"), bytesFromClient[1])
            print("S: com-0 accept", localIP)
            bytesFromClient = UDPServerSocket.recvfrom(bufferSize)
            if bytesFromClient[0] == str.encode("Clientacc"):
                print("C: com-0 accept")
                print("Connection successful...")

                #Log the Successful handshake
                f = open("logFile.txt", "a")
                f.write("Client has connected with IP: ")
                f.write("{}".format(address))
                f.write(todaysDate)
                f.write("\n")
                f.close()
                chat(message, address)
    except:
                time.sleep(0.1)