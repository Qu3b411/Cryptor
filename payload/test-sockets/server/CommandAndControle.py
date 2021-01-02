#!/usr/bin/env python3
import server; 
import sys

print(str(server.secure_recv()))
print(str(server.secure_recv()))
print(str(server.secure_recv()))
server.secure_send(bytearray(b'hello world'),11)
server.secure_send(bytearray(b'hello world this is the server'),30)

