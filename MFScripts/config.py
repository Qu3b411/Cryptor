#!/usr/bin/env python3
# This Script is responsible for generating the config file used durring
# the build process of the cryptor
#
# Copyright (C) 2020  @Qu3b411
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#


import sys
import re
import os
def IPtest(IPADDR):
    if (r1 := re.match( "^\s*((?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])\."\
                        "(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])\."\
                        "(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])\."\
                        "(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9]))\s*$", IPADDR)):
        return(r1.group(1));

def LogPrompt(st):
    print ("\t"+os.path.basename(__file__)+">>\t"+st);

def config():
    LogPrompt("Checking for configuration file (conf)...");
    try:
        with open("./conf") as f:
            LogPrompt("Configuration file (conf) exists in expected location!")
    except IOError:
        LogPrompt("conf file does not exist, Running conf generation now");
        try:
            with open("./conf", "w+") as f:
                IP = input("\t"+os.path.basename(__file__)+">>\tEnter an IP address for your server: ");
                while (not (IP := IPtest(IP))):
                    IP = input("\t\t\tInvalid IP address!\n"
                    "\t"+os.path.basename(__file__)+">>\tEnter an IP address for your server: ");
                f.write("IPADDR_SVR = " + str(IP)+"\n");
                PORT = int(input("\t"+os.path.basename(__file__)+">>\tEnter the Port number for your server:"));
                while( not (PORT>0 and PORT<65535)):
                    PORT = int(input("\t\t\tInvalid Port Number!\n"
                            "\t"+os.path.basename(__file__)+">>\tEnter the Port number for your server: "));
                f.write("PORT_SVR = " + str(PORT)+"\n");
                CTRL_PORT = int(input("\t"+os.path.basename(__file__)+">>\tEnter the server control port number (port used for API calls):"));
                while( not (CTRL_PORT>0 and PORT<65535)):
                    CTRL_PORT = int(input("\t\t\tInvalid Port Number!\n"
                            "\t"+os.path.basename(__file__)+">>\tEnter the server control port number for your server: "));
                f.write("CTRL_PORT = " + str(CTRL_PORT) + "\n");
                LogPrompt("Writing additional default configurations to (Conf), These settings are recommended");
                LogPrompt("Chose a security level\n\t\t\t\t 1 - RSA 2048 / AES 128\n\t\t\t\t 2 - RSA 3072 / AES 192 \n\t\t\t\t 3 - RSA 4096 / AES 256")
                securityLevel = 0;
                while securityLevel < 1 or securityLevel > 3:
                    securityLevel = int(input("\t"+os.path.basename(__file__)+">>\tEnter Security Level: " ))
                
                if securityLevel == 1: 
                    LogPrompt("AES key length written to (Conf), 128 bit (16 bytes)");
                    f.write("AES_KEY_LEN = 16\n")
                    LogPrompt("RSA key length written to (Conf), 2048 bit (256 bytes)");
                    f.write("RSA_KEY_LEN = 2048\n")
                elif securityLevel == 2:
                    LogPrompt("AES key length written to (Conf), 192 bit (24 bytes)");
                    f.write("AES_KEY_LEN = 24\n")
                    LogPrompt("RSA key length written to (Conf), 3072 bit (384 bytes)");
                    f.write("RSA_KEY_LEN = 3072\n")
                elif securityLevel == 3:
                    LogPrompt("AES key length written to (Conf), 256 bit (32 bytes)");
                    f.write("AES_KEY_LEN = 32\n")
                    LogPrompt("RSA key length written to (Conf), 4096 bit (512 bytes)");
                    f.write("RSA_KEY_LEN = 4096\n")


            LogPrompt("Conf file generated");
        except IOError:
            LogPrompt("Conf file could not be generated");
# os.chdir('../');
config();
