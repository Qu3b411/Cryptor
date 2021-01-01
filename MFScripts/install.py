import site
import subprocess
import sys
import os
import csv


_all_ = [
        "pycryptodome"
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
    with open (site.USER_SITE+"/CryptorSVR.pth", "w") as pathFile:
            pathFile.write(os.getcwd()+"/SVR_SRC")

    if platform == 'win32':
        install(windows)
        print(os.path())
        for path in str(os.environ['PATH']).split(";"):
            print(path) 

    if platform.startswith('linux'):
        install(linux)
        svrPath = os.getcwd()+"/SVR_SRC"
        print(svrPath)
    if platform == 'darwin': # MacOS
        install(darwin)
