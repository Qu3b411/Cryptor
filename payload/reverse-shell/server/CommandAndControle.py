#!/usr/bin/env python3
import server; 
import sys

while(True):
    print(server.secure_recv().decode('ascii'),end="")
    Command = input();
    server.secure_send(Command.encode("utf8"),len(Command))
