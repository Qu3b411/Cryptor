#!/usr/bin/env python3
import server; 
import sys

print(server.secure_recv().decode('ascii'))
