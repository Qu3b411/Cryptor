#!/usr/bin/env python3
import server; 
import sys
import functools

print = functools.partial(print, flush=True)
class payload(server.Victim):
    def run(self):
        print("Launching calc")

if __name__ == "__main__":
    server.run(payload)
