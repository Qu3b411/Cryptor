# TODO
**Improve documentation wherever possible, enhance clerity and limit abstractions**
### Server Side

~~1. create a listening socket is SVR_SRC port Defined PORT_SVR.~~

~~2. Retrive Encrypted OTP from client and, then rsa decrypt~~

~~3. decrypt OTP.~~

~~4. base64 decode AES key~~

~~5. xor OTP witk AES key~~

~~6.  send (OTP ^ AES) to client~~

### Client side (CS_SRC)

~~1. Connect to server~~

~~2. send the eencrypted OTP to the server~~

~~3. retrive the AES key from the server.~~

~~4. use the OTP to retrive the key for encryption~~

6. decrypt the payload (START_OF_PAYLOAD --> END_OF_PAYLOAD)

