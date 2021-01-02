# C2 Payload Cryptor

NOTES:
I'm starting work on a reverse shell; this is not complete, but the directory is in the payloads. I'm still not sure how I will write this payload, but it isn't a simple redirection of stdin/stdout. Please don't expect that to run if you set that as the payload.

Linux compatibility is not here yet, but it is close; @fox3455 will be working on developing that element of the functionality in the LinuxAdaptation branch.

Finally, I would love any help in developing new and unique payloads. I wanted a modular method for creating payloads that anyone could use. 

---
## Getting started
Build this on a windows 10 image for this payload to work.
Requires ```git-bash```, ```Python 3.8 or greater```, and ```GCC``` (I would recommend MingW32), make sure to install pip for Python so the install script can install the required packages.

### Understanding payloads
Specifying the payload to build requires the Payload=payload-name directive to be set on the command line during a make. The containing directory names a payload.
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
the client components are written in C, whereas the server components are Python. 

To get started building your first payload, you need a client component. The client should be in the client directory of the payload being defined.

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
your server component should be in the server directory of the defined payload, 
```python3
#!/usr/bin/env python3
import server
# Your imports here

# your server code here
```
**C functions/definitions**

The C header will import two functions.

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
Additionally, multiple function initializers have been defined to abstract the payload section attribute so you (the author) can focus on the mechanics of your payload without the need to focus on the underlying mechanics of the sockets/cryptographic implementations. The naming convention is PL_type; these are the definitions.
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
Understanding these definitions exist or knowing their equivalent definitions is enough for you to begin authoring payloads.

**Python Functions**

In Python, there are two functions of interest to you as the payload developer.


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
All sockets and cryptographic primitives used are to be managed by the constructors/destructors. You are responsible for the payload development, 
## Building your payload

The makefile will install all additional packages for you during the build process. The current structure allows for different payloads to be developed and used on the same underlying cryptor/comms channels. **[NOTE: the current default payload built is the test-sockets.]**

With all of the requirements installed, you can build the project as either ```Debug``` or ```Release```.
  -     make Release 
  -     make Debug

To specify a different payload set the Payload make variable
  -     make Releas Payload='your-payload-here'
  -     make Releas Payload='your-payload-here'

**During the build, you will encounter  multiple prompts for configuration information**

First, the configuration script will prompt you for an IP address for testing. You can enter ```127.0.0.1```, for **AUTHORIZED** penetration testing; this is where you will set the server's IP address that will act as your c2. 

The next prompt is for you to specify a port number on which your server will be listening. 

The final configuration will be to specify a security level; possible levels are 
    1 - rsa 2048/AES128
    2 - rsa 3072/AES192
    3 - rsa 4096/AES256

To define a new configuration issue.
-      make Conf
This command will prompt you for the information mentioned above to create a new Conf file. Once this file exists, you will not be prompted for this information again. 
**Editing the Conf.default** file is another way to configure your server. Make a copy of ```Conf.default``` and rename it conf. From here, more options exist. edit with caution

to remove everything besides the default files issue
-       make Clean
This command will remove everything generated during compile time. Including auto-generated header files, bin directories, and __pycache__.

# WARNING!
> The use of this for any purposes outside of Authorized Penetration testing and or Educational purposes is strictly forbidden! **DO NOT** use this software in any capacity that is not **Authorized**, if your intent is malicious **You stand alone**. You will not gain support from me or others whose interests are strictly academic.
> YOU ARE EXPRESSLY ALLOWED TO USE THIS SOFTWARE IN THE FOLLOWING MANNER
* Academic research - This requires strict environmental controls to prevent any release of malicious code 
* Authorized and controlled Penetration testing - where the payloads have a controlled scope that prevents exposure to nonauthorized targets
* educational purposes - in such capacity, you must have a controlled lab environment.

> If you use this software in an unauthorized manner, You act of your own volition, and in such capacity, I disclaim any responsibility for your actions. 
