#!/usr/bin/env python3
import server; 
import sys
import functools

print = functools.partial(print, flush=True)
class payload(server.Victim):
    def run(self):
        print(str(self.secure_recv()))
        print(str(self.secure_recv()))
        print(str(self.secure_recv()))
        self.secure_send(bytearray(b'hello world'),11)
        self.secure_send(bytearray(b'hello world this is the server'),30)
        while True:
            print(str(self.getCommandFromQueue()))
if __name__ == "__main__":
    server.run(payload)
