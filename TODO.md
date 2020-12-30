# TODO
**Improve documentation wherever possible, enhance clerity and limit abstractions**

**Clean up file structure, abstract some of the functionality**

**Add SVR_SRC to the system environment in install.py**

### Server Side

~~1. create a listening socket is SVR_SRC port Defined PORT_SVR.~~

~~2. Retrive Encrypted OTP from client and, then rsa decrypt~~

~~3. decrypt OTP.~~

~~4. base64 decode AES key~~

~~5. xor OTP witk AES key~~

~~6.  send (OTP ^ AES) to client~~

~~7. write initialization code for a secure_recieve() function~~

~~8. write initialization code for a secure_send() function~~

**9. re-write the server to use classes and inheritence.**
>    This seams like the best meathod to abstract the server functionality

### Client side (CS_SRC)

~~1. Connect to server~~

~~2. send the eencrypted OTP to the server~~

~~3. retrive the AES key from the server.~~

~~4. use the OTP to retrive the key for encryption~~

~~5. import AES key into bcrypt handle~~

~~6. decrypt the payload (START_OF_PAYLOAD --> END_OF_PAYLOAD)~~

~~7. Destroy keys~~

~~8. write a secure_send() function initialized by  a constructor priority 102~~

~~9. write a secure_recieve() function initialized by a constructor priority 102~~

### Add Linux varient

~~1. Edit makefile~~
```
    a. Change echo to bash - DONE 
    b. Change the linker script (after -T) to the Linux specific. - DONE
```  
~~2. Edit linker.id~~
```
    a. Copy from .txt to End_of_Payload - DONE
    b. Add that to the linker.id dump - DONE
```
3. cryptPayload.py
```
    a. Change pefile (Windows uses PE while linux uses ELF)
```    
4. Edit clientHeader.h
```
    a. Add elif logic on all Windows and Linux specific libraries
    b. Initiate socket in Linux friendly format (started in constructor and closed by destructor)
```
5. Add new python libraries to ~~quirements.txt~~ install.py



