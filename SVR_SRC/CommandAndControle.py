import server; 
from C2 import *
import socket
import sys

cli = socket.socket()
cli.connect(('127.0.0.1', CTRL_PORT))
  
def sendStr(SendStr):
    length = len(SendStr)
    cli.send((length).to_bytes(8,byteorder="big")) # UINT32 4 bytes.
    cli.recv(1) #Sync
    cli.send(SendStr)
    cli.recv(1) #Sync

def recvStr():
    msgSZ = int.from_bytes(cli.recv(8),byteorder='big',signed=False)
    cli.send(b"\x01")
    MSG = cli.recv(msgSZ)
    cli.send(b"\x01")
    return MSG.decode()

def clientInterface():
    print(recvStr())
    cli.close()

if __name__ == '__main__':
    clientInterface()
