#!/usr/bin/env python3
import server; 
import string;
import sys

while(True):
    print(str(server.secure_recv(),'ascii'),end="")
    Command = input();
    server.secure_send(Command.encode("utf8"),len(Command))
