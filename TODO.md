# TODO
**Improve documentation wherever possible, enhance clerity and limit abstractions**
### Server Side
	1. ~~~create a listening socket is ```SVR_SRC``` port Defined ```PORT_SVR```.~~~
	2. retrive Encrypted OTP from client and, base64 decode then rsa decrypt
	3. decrypt OTP. 
	4. base64 decode AES key
	5. xor OTP witk AES key
	6. base 64 and send (OTP ^ AES) to client
### Client side (CS_SRC)
	1. WTF IS GOING ON WITH LINE 79 IN CL_SRC/main.c i thought the crypto was working but :(
	2. ~~~Connect to server~~~
	3. base64 encode and send the eencrypted OTP to the server
	4. retrive the AES key from the server and base 64 decode.
	5. use the OTP to retrive the key for encryption
	6. decrypt the payload (START_OF_PAYLOAD --> END_OF_PAYLOAD)
