import subprocess
import sys

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
    if platform == 'win32':
        install(windows)
    if platform.startswith('linux'):
        install(linux)
    if platform == 'darwin': # MacOS
        install(darwin)