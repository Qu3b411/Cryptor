import pip

_all_ = [
        "pycryptodomex"
]
#Any Windows specific packages
windows = ["pefile",]

#Any Linx specific packages
linux = [""]

#Any MacOS specific packages
darwin = [""]

#This defines the peramiters for pip
def install(packages):
    for package in packages:
        pip.main(['install', package])

#Install all packages, then move to logic for OS specific packages
if __name__ == '__main__':

    from sys import platform

    install(_all_) 
    if platform == 'windows':
        install(windows)
    if platform.startswith('linux'):
        install(linux)
    if platform == 'darwin': # MacOS
        install(darwin)
