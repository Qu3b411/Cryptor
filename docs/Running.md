# Running the Payload Server.

This program has a simple terminal interface while I build out the API; the API will work in JSON.

Step one, open a console and run the server under the appropriate Payload directory.

![CommandAndControle](https://github.com/Qu3b411/Cryptor/blob/master/docs/img/Running%20Payload%20Server.PNG)

The server will initialize and begin listening for new victims to connect.

# Runnng Clients

It is highly advised that you use the Release versions of payloads, Some Debug flags used in the Debug variant cause errors. Once the makefile has been run, and the payload is built, you can find the resulting binary under the bin directory in the project's root. If you have configured your server to run on localhost 127.0.0.1, simply running a payload binary is enough to connect a handful of victims to your C2 server. 

![Victims](https://github.com/Qu3b411/Cryptor/blob/master/docs/img/Connecting%20Victims.PNG)

# Controle Clients
The server now has multiple connected victims; however, we could not send commands to the victim environment without a control client. The command and control client is located under ```SVR_SRC``` as ```CommandAndControle.py```

![CommandAndControleClient](https://github.com/Qu3b411/Cryptor/blob/master/docs/img/CommandAndControle%20client.PNG)

### Targeting all clients:
The format of the commands are simple; one must first specify a Target, then a Command. To target all connected victims, one may use a target of \*. Next, specify a Command, a simple one for the reverse shell could be ```Command="cd bin"``` or ```Command=dir```

```Target=* Command="cd bin```

![TargetAll](https://github.com/Qu3b411/Cryptor/blob/master/docs/img/TargetAll.PNG)

```
Known issue:
This issue has continued to persist, and I'm unable to pin down what's going on. Sometimes a string is mutilated in the sending from client to server. I'm unaware of what could be causing it, but I would be very appreciative of anyone that could help me identify where this bug is originating
```
### Targeting individual clients:
An individual target can be specified in the following manner ```Target=('ip-address-of-victim', port #)```

![TargetIndividual](https://github.com/Qu3b411/Cryptor/blob/master/docs/img/CommandToIndividual.PNG)

