# C2 Payload Cryptor
---
## Getting started
build this on a windows 10 image for this payload to work.
Requires ```git-bash```, ```Python 3```, and ```gcc``` (I would recommend MingW32), make sure to install pip for python so you can install the required packages. 

Install all required modules, open git bash terminal and run ```py -m pip install -r ./requirements.txt``` to install all the required modules.

If all of the requirements are installed you can build the project as either ```Debug``` or ```Release```.
  -     make Release 
  -     make Debug
 **During the build you will be prompted for configuration information**  first the configuration script will prompt you for an IP address, for testing you can enter ```127.0.0.1```, for **AUTHORIZED** penetration testing this is where you will set the IP address of the server that will act as your c2. next you will be prompted for a port number, this defines the port on which your server will be listening. 
To define a new configuration issue.
-      Make Conf
This will prompt you for the aforementioned information to create a new Conf file. once this file exists you will not be prompted for this information again. 
**Editing the Conf.default** file is another way to configure your server. make a copy of ```Conf.default``` and rename it conf. from here more options exist, however it is recommended that you keep the defaults as they are the most secure 

the payload up until this point is an empty shell open to whatever payloads you can think up, you can find the **C** file for the client configuration in ```./CL_SRC/main.c``` this is where the payload section exists,

to remove everything besides the default files issue
-       make clean
this will remove everything that was generated during compile time, this includes auto-generated header files.

# This is still incomplete!
 I am still working on the crypto and will likely be changing and improving it as time permits. comments within the ```./CL_SRC/main.c``` file indicate what still has to be done to get this project to a working state, note the server has to be completed to finish the client. 

# WARNING!
> The use of this for any purposes outside of Authorized Penetration testing (and/or) Educational purposes is strictly forbidden! **DO NOT** use this software in any capacity that is not **Authorized**, if your intent is malicious **You stand alone**. You will not gain support from me or others who's interest is strictly academic.
> YOU ARE EXPRESSLY ALLOWED TO USE THIS SOFTWARE IN THE FOLLOWING MANNER
* Academic research - This requires strict environmental controls to prevent any release of malicious code 
* Authorized and controlled Penetration testing - where the payloads have a controlled scope that prevents exposure to non authorized targets
* educational purposes - in such capacity you must have a controlled lab environment.

> If you use this software in an unauthorized manner, You act of your own volition and in such capacity, I disclaim any responsibility for your actions. 
