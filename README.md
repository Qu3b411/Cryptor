# C2 Payload Cryptor
---
## Getting started
build this on a windows 10 image for this payload to work.
Requires ```git-bash```, ```Python 3.8 or greater```, and ```gcc``` (I would recommend MingW32), make sure to install pip for python so you can install the required packages. 

### Understanding payloads
payloads are specified in the payloads director
```
(.)root
    |
    |-->payload
    |      |
    |      |-->test-socket
    |      |       |
    |      |       |--> client
    |      |       |
    |      |       |--> server
    |      |
    |      |--> <YOUR-PAYLOAD-GOES0-HERE>
    |      |       |
    |      |       |--> client
    |      |       |
    |      |       |--> server
```
the client components are written in C, whereas the server components are written in Python. 

To get started building your first payload you need a client component, the client should be in the client directory of the payload being defined

main.c
```C
#include "clientHeader.h"
/*
  your includes here
*/
PL_int main()
{
/*
  your code here
*/
}
```
your server component should be in the sever directory of the payload being defined, 
```python3
#!/usr/bin/env python3
import server
# Your imports here

# your server code here
```
**C functions/definitions**

The C header will import two functions

**int send_secure(BYTES* buffer, int* len)**
```
  buffer: the bytes to send to the server
  len: the length of the buffer to send
  
  returns 0 on success
```
**BYTE* recv_secure()**
```
  returns a pointer to the buffer returned from the server 
```
Additionally this hader defines multiplev function initializers that abstract the payload section attribute so you (the author) can focus on the mechanics of your payload without the need to focus on the underlying mechanics of the sockets/cryptographic implentations, the naming convention is PL_type, these are the definitions.
```C
#define PL_void			__attribute__((section(".payload"))) void
#define PL_char 		__attribute__((section(".payload"))) char 
#define PL_unsigned_char 	__attribute__((section(".payload"))) unsigned char 
#define PL_short 		__attribute__((section(".payload"))) short
#define PL_unsigned_short 	__attribute__((section(".payload"))) unsigned short
#define PL_int		 	__attribute__((section(".payload"))) int
#define PL_unsigned_int		__attribute__((section(".payload"))) unsigned int
#define PL_long		 	__attribute__((section(".payload"))) long 
#define PL_unsigned_long 	__attribute__((section(".payload"))) unsigned long
#define PL_long_long	 	__attribute__((section(".payload"))) long long
#define PL_unsigned_long_long 	__attribute__((section(".payload"))) unsigned long long
#define PL_float	 	__attribute__((section(".payload"))) float
#define PL_double	 	__attribute__((section(".payload"))) double
#define PL_long_double	 	__attribute__((section(".payload"))) long double
#define PL_		 	__attribute__((section(".payload")))
```
Understanding these definitions exist, or knowing their equvilant definitions is enough for you to begin authoring payloads.

**Python Functions**

In python their are two functions of interest to you as the payload developer


**send_secure(buf: bytes, length: int)
```
  buf: the bytes to send to the server
  length: the length of the buffer to send
  
  returns 0 on success
```
**bytes recv_secure()**
```
  returns a pointer to the buffer returned from the server 
```
these are the complimentary functions from the server 

### [NOTE]
All sockets and cryptographic primitives are managed by the constructors/destructors. this truley allows you to run make and start at the fun part of payload development without managing the underlying communications.

## Building your payload

All additional required packages will be installed for you during the buid process, The current structure allows for different payloads to be developed. **[NOTE: the current default payload built is the test-sockets.]**

If all of the requirements are installed you can build the project as either ```Debug``` or ```Release```.
  -     make Release 
  -     make Debug

To specify a different payload set the Payload make variable
  -   make Releas Payload='your-payload-here'
  -   make Releas Payload='your-payload-here'

**During the build you will be prompted for configuration information**
first the configuration script will prompt you for an IP address, for testing you can enter ```127.0.0.1```, for **AUTHORIZED** penetration testing this is where you will set the IP address of the server that will act as your c2. 

next you will be prompted for a port number, this defines the port on which your server will be listening. 

the final configuration will be to specify a security level, possible levels are 
    1 - rsa 2048/AES128
    2 - rsa 3072/AES192
    3 - rsa 4096/AES256

by entering 1 you will get the lowest level of security offered without manually modifying the conf file, however it is strongley reccommended that one sette for a higher security offering.

To define a new configuration issue.
-      make Conf
This will prompt you for the aforementioned information to create a new Conf file. once this file exists you will not be prompted for this information again. 
**Editing the Conf.default** file is another way to configure your server. make a copy of ```Conf.default``` and rename it conf. from here more options exist, however it is recommended that you rely on a default configuration

to remove everything besides the default files issue
-       make Clean
this will remove everything that was generated during compile time, this includes auto-generated header files.

# WARNING!
> The use of this for any purposes outside of Authorized Penetration testing (and/or) Educational purposes is strictly forbidden! **DO NOT** use this software in any capacity that is not **Authorized**, if your intent is malicious **You stand alone**. You will not gain support from me or others who's interest is strictly academic.
> YOU ARE EXPRESSLY ALLOWED TO USE THIS SOFTWARE IN THE FOLLOWING MANNER
* Academic research - This requires strict environmental controls to prevent any release of malicious code 
* Authorized and controlled Penetration testing - where the payloads have a controlled scope that prevents exposure to non authorized targets
* educational purposes - in such capacity you must have a controlled lab environment.

> If you use this software in an unauthorized manner, You act of your own volition and in such capacity, I disclaim any responsibility for your actions. 
