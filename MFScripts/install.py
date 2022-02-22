#!/usr/bin/env python3

# this script installs dependecnies and adds the appropriate
# system paths for the server imports to work as intended
import site
import subprocess
import sys
import os
import csv
# import random
# import string
from os.path import exists

_all_ = [
        "pycryptodome",
        "simplejson",
        "django",
        "mysql"
]
#Any Windows specific packages
windows = ["pefile",]

#Any Linx specific packages
linux = ["pyelftools"]

#Any MacOS specific packages
darwin = [""]

def install(packages):
    for package in packages:
        if package != "":
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

#Install all packages, then move to logic for OS specific packages
if __name__ == '__main__':

    from sys import platform
    install(_all_)    
    if not os.path.exists(site.USER_SITE):
        os.makedirs(site.USER_SITE)
    with open (site.USER_SITE+"/CryptorSVR.pth", "w+") as pathFile:
        pathFile.write(os.getcwd()+"/SVR_SRC")
    if platform == 'win32':
        install(windows)
    if platform.startswith('linux'):
        install(linux)
    if platform == 'darwin': # MacOS
        install(darwin)
