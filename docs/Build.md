# This documentation is for building the most recent version.
## If building for the first time
**Step 1:** Discover what payload you wish to make. 
1. At you bash terminal navigate to the root directory of the project
2. Type ```ls ./payload```
3. inside you will see a mkPayload. py script and several directories, Each directory represents a payload.

![IdentifyPayloads](https://github.com/Qu3b411/Cryptor/blob/master/docs/img/B1.PNG)

**Step 2:** running make.
1. you will liely be using a varient of gcc ```mingw32-make.exe```
2. Specify the name of the Payload I.E. ```Payload=reverse-shell```
3. Build under Release, the debug branch is not stable, debug symbols become corrupted interfearing with program execution

``` mingw32-make.exe Payload=reverse-shell Release``` 

**Step 3:** the makefile will run ```config.py``` You will be prompted for various settings.
1. You will first be prompted for the server IP address, for testing and demonstration purposes use ```127.0.0.1```. Using this IP address also ensures that the binary cannot run on unauthorized machines. 
2. You will next be prompted for the server's port number, this is the port number that victims connect to. I tend to use the port 8080 for testing, The traffic to this port is encrypted.
3. You will then be prompted for the controle port number, this is the port by which clients will post API calls, for now this is working but it is meant for local host dev. The traffic to this port is unencrypted. I tend to use the port ```9000```.
4. Finally you will be prompted to chose a security level, 1 corresponds to RSA 2048/AES 256, 2 corresponds to RSA 3072/AES192, and finally 3 corresponds to RSA 4096 / AES 256.
5. After hitting enter all of the keys will be generated, and the ```.payload``` section will be encrtypted. 

![BuildingNew](https://github.com/Qu3b411/Cryptor/blob/master/docs/img/B2.PNG)
### At this point your binary will be generated in the bin directory, and all other configuration files will have been generated

## If re-building
The first two steps are the same due to the design of the make file

**Step 1:** Discover what payload you wish to make. 
1. At you bash terminal navigate to the root directory of the project
2. Type ```ls ./payload```
3. inside you will see a mkPayload. py script and several directories, Each directory represents a payload.

![IdentifyingPayloads](https://github.com/Qu3b411/Cryptor/blob/master/docs/img/B1.PNG)

**Step 2:** running make.
1. you will liely be using a varient of gcc ```mingw32-make.exe```
2. Specify the name of the Payload I.E. ```Payload=reverse-shell```
3. Build under Release, the debug branch is not stable, debug symbols become corrupted interfearing with program execution

``` mingw32-make.exe Payload=reverse-shell Release``` 

**Step 3:** ```Keygen.py``` will discover keys configured for this payload, you will be prompted on if you wnat to generate new keys. This may be useful for generating the same binary with a different signature if that is the goal.
1. If you want to generate new keys for this payload type ```Y```
2. If you don't want to generate new keys for this payload type ```N```

![Rebuilding](https://github.com/Qu3b411/Cryptor/blob/master/docs/img/B3.PNG)

### At this point your binary will be generated in the bin directory, and all other configuration files will have been generated

## If you want to change the configuration before re-building

**Option 1**

**Step 1:** manually modify the ```conf``` file located in the root directory of the project.
**Step 2:** re-build the payload.

![Modify conf](https://github.com/Qu3b411/Cryptor/blob/master/docs/img/B4.PNG)

**Option 2**

**Step 1:** Make Clean if using mingw32 this would be ```mingw32-make.exe Clean```
**Step 2:** Build the new payload as if this were a fresh git clone. 

![Rebuilding](https://github.com/Qu3b411/Cryptor/blob/master/docs/img/B5.PNG)
