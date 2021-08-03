#!/usr/bin/env python3
import os

CurrentDir= os.getcwd();
PayloadName = input("Please enter the name of your new payload: ")
finalDir=os.path.join(CurrentDir,PayloadName)

cliPath = os.path.join(PayloadName,r'client')
svrPath = os.path.join(PayloadName,r'server')
if not os.path.exists(finalDir):
    os.makedirs(cliPath)
    os.makedirs(svrPath)
    try:
        with open(os.path.join(cliPath,r'main.c'),"w+") as f:
            f.write("""#include "clientHeader.h"
#include <stdlib.h>

/*
 *	****************************************************************
 *	YOUR PAYLOAD GOES HERE, THIS IS WHERE YOUR DEVELOPMENT WORK WILL
 *	BEGIN. HAVE FUN
 *	****************************************************************
 *
 * 	USE PLStr to secure all your binary strings
 */
 PL_int main(){
	
}""")
    except IOError:
        print ("Error in generating new payload")

    try:
        with open(os.path.join(svrPath,r'CommandAndControl.py'),"w+") as f:
            f.write("""#!/usr/bin/env python3
import server as server; 

class victim_payload(server.victim):
    def __init__(self):
        super().__init__()


    def payload(self):
        #Your payload goes here

v = victim_payload();
v.payload()""")
    
    except IOError:
        print("Error in generating new payload")

