#!/usr/bin/env python3
import server as server; 
class victim_payload(server.victim):
    def __init__(self):
        super().__init__()
    def payload(self):
        #Your payload goes here
v = victim_payload();
v.payload()